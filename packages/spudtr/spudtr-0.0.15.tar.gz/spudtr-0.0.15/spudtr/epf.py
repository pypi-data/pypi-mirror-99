"""utilities for epoched EEG data in a pandas.DataFrame """
from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import bottleneck as bn

from spudtr.filters import _design_firwin_filter, fir_filter_dt

EPOCH_ID = "epoch_id"  # default epoch ID column
TIME = "time"  # default time column


def _validate_epochs_df(epochs_df, epoch_id=EPOCH_ID, time=TIME):
    """check form and index of the epochs_df is as expected

    Parameters
    ----------
    epochs_df : pd.DataFrame

    epoch_id : str (optional, default=epf.EPOCH_ID)
        column name for epoch indexes

    time: str (optional, default=epf.TIME)
        column name for time stamps

    """
    for key, val in {"epoch_id": epoch_id, "time": time}.items():
        if val not in epochs_df.columns:
            raise ValueError(f"{key} column not found: {val}")


def _epochs_QC(epochs_df, data_streams, epoch_id=EPOCH_ID, time=TIME):
    """Quality control for spudtr format epochs, returns epochs_df on success"""

    # epochs_df must be a Pandas DataFrame.
    if not isinstance(epochs_df, pd.DataFrame):
        raise ValueError("epochs_df must be a Pandas DataFrame.")

    # data_streams must be a list of strings
    if not isinstance(data_streams, list) or not all(
        isinstance(item, str) for item in data_streams
    ):
        raise ValueError("data_streams should be a list of strings.")

    # all channels must be present as epochs_df columns
    missing_channels = set(data_streams) - set(epochs_df.columns)
    if missing_channels:
        raise ValueError(
            "data_streams should all be present in the epochs dataframe, "
            f"the following are missing: {list(missing_channels)}"
        )

    # check no duplicate column names in index and regular columns
    names = list(epochs_df.index.names) + list(epochs_df.columns)
    if len(names) != len(set(names)):
        raise ValueError("Duplicate column names not allowed.")

    # epoch_id and time must be the columns in the epochs_df
    _validate_epochs_df(epochs_df, epoch_id=epoch_id, time=time)

    # check values of epoch_id in every time group are the same, and
    # unique in each time group. Make our own copy so we are immune to
    # modification to original table
    table = epochs_df.copy().reset_index().set_index(epoch_id).sort_index()
    assert table.index.names == [epoch_id]

    snapshots = table.groupby([time])

    # check that snapshots across epochs have equal index by transitivity
    prev_group = None
    for idx, cur_group in snapshots:
        if prev_group is not None:
            if not prev_group.index.equals(cur_group.index):
                raise ValueError(
                    f"Snapshot {idx} differs from "
                    f"previous snapshot in {epoch_id} index:\n"
                    f"Current snapshot's indices:\n"
                    f"{cur_group.index}\n"
                    f"Previous snapshot's indices:\n"
                    f"{prev_group.index}"
                )
        prev_group = cur_group

    def list_duplicates(seq):
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set(x for x in seq if x in seen or seen_add(x))
        # turn the set into a list (as requested)
        return list(seen_twice)

    if not prev_group.index.is_unique:
        dupes = list_duplicates(list(prev_group.index))
        raise ValueError(
            f"Duplicate values of epoch_id in each" f"time group not allowed:\n{dupes}"
        )
    return epochs_df


def _hdf_read_epochs(epochs_f, h5_group, epoch_id=EPOCH_ID, time=TIME):
    """read tabular hdf5 epochs file, return as pd.DataFrame

    .. deprecated:: 0.0.9
       Use native pandas HDF functions instead. Will be removed in 0.0.11


    Parameters
    ----------
    epochs_f : str
        name of the recorded epochs file to load

    h5_group : str
        name of h5 group key

    Return
    ------
    df : pd.DataFrame
        columns in INDEX_NAMES are pd.MultiIndex axis 0
    """
    warnings.warn(
        "_hdf_read_epochs() is unused, untested, and deprecated in spudtr.epf v0.0.9 and will be removed in v0.0.11",
        DeprecationWarning,
    )

    if h5_group is None:
        raise ValueError("You have to give h5_group key")
    else:
        epochs_df = pd.read_hdf(epochs_f, h5_group)

    _validate_epochs_df(epochs_df, epoch_id=epoch_id, time=time)
    return epochs_df


def _find_subscript(times, start, stop):
    """start stop interval includes end both end time stamps

    This makes the timestamp interval open left and right, 
    [start, stop] when slicing with pandas and open left, 
    closed right, [start, stop) when slicing with numpy.
    """
    istart = np.where(times >= start)[0]
    if len(istart) == 0:
        raise ValueError(
            "start is too large (%s), it exceeds the largest " "time value" % (start,)
        )
    istart = int(istart[0])

    istop = np.where(times <= stop)[0]
    if len(istop) == 0:
        raise ValueError(
            "stop is too small (%s), it is smaller than the "
            "smallest time value" % (stop,)
        )
    istop = int(istop[-1])
    if istart >= istop:
        raise ValueError(
            "Bad rescaling slice (%s:%s) from time values %s, %s"
            % (istart, istop, start, stop)
        )
    return istart, istop


# ------------------------------------------------------------
# user API
# ------------------------------------------------------------


def check_epochs(epochs_df, data_streams, epoch_id=EPOCH_ID, time=TIME):
    """check epochs data are in spudtr format

    Parameters
    ----------
    epochs_df : pd.DataFrame

    data_streams: list of str
        the columns containing data
        
    epoch_id : str, optional
        column name for the epoch index

    time: str, optional
        column name for the time stamps


    Raises
    ------
    Exception 
       diagnostic for what went wrong

    """

    _ = _epochs_QC(epochs_df, data_streams, epoch_id=epoch_id, time=time)


def center_eeg(epochs_df, eeg_streams, start, stop, epoch_id=EPOCH_ID, time=TIME):

    """center (a.k.a. "baseline") EEG amplitude on mean amplitude in [start, stop)
    

    Parameters
    ----------
    epochs_df : pd.DataFrame
        must have epoch_id and time columns

    eeg_streams: list of str
        column names to apply the transform

    start,stop : int
        basline interval time values, `start <= t <= stop`

    epoch_id : str, optional
        column to use for the epoch index

    time : str, optional
        column to use for the time stamp index


    Returns
    -------
    centered_epochs_df : pd.DataFrame
       each epoch and channel time series centered on the [start, stop)
       interval mean amplitude

    Notes
    -----

    The `start`, `stop` values pick the smallest and largest
    timestamps in the interval, i.e., [start_stamp, stop_stamp], but
    since the data are sliced with np.arange, the upper bound is not
    included, i.e., start_stamp <= timestamps < stop_stamp.  So, for
    instance, start=-200, stop=0, would include timestamps at -200,
    -199, ... -1, but not 0. 

    """

    _epochs_QC(epochs_df, eeg_streams, epoch_id=epoch_id, time=time)

    # calculate the row-index vector to slice the centering intervals
    n_times = len(epochs_df[time].unique())
    n_epochs = len(epochs_df[epoch_id].unique())
    times = epochs_df[time].unique()
    istart, istop = _find_subscript(times, start, stop)
    center_idxs = np.array(
        [
            np.arange(istart + (i * n_times), istop + (i * n_times))
            for i in range(n_epochs)
        ]
    ).flatten()

    # use pandas iloc index slicing then groupby epoch_id to compute means
    mns = epochs_df.iloc[center_idxs, :].groupby(epoch_id)[eeg_streams].mean()

    # inflate the means to the shape of the data and subtract in place, not sure if view() saves memory
    centered_epochs_df = epochs_df.copy()
    centered_epochs_df[eeg_streams] -= np.repeat(mns.to_numpy().view(), n_times, axis=0)

    return centered_epochs_df


def drop_bad_epochs(epochs_df, bads_column, epoch_id=EPOCH_ID, time=EPOCH_ID):
    """Quality control data slicer, excludes previously tagged artifact epochs

    All epochs tagged with a non-zero quality code on the specified
    `bads_column` at the time stamp == 0 are excluded.


    Parameters
    ----------
    epochs_df : pd.DataFrame
        must have epoch_id and time row index names

    bads_column : str
        column name with QC codes: non-zero == drop

    epoch_id : str, optional
        column name for epoch indexes

    time: str, optional
        column name for time stamps

    Returns
    -------
    good_epochs_df : pd.DataFrame
       subset of the epochs with code 0 on `bads_column` at timestamp == 0

    """

    _epochs_QC(epochs_df, [bads_column], epoch_id=epoch_id, time=time)

    # get the group of time == 0
    group = epochs_df.groupby([time]).get_group(0)

    good_idx = list(group[epoch_id][group[bads_column] == 0])

    good_epochs_df = epochs_df[epochs_df[epoch_id].isin(good_idx)].copy()

    return good_epochs_df


def re_reference(epochs_df, eeg_streams, ref, ref_type, epoch_id=EPOCH_ID, time=TIME):
    """Convert EEG data recorded with a common reference to a different reference

    .. warning::

       These transforms are intended for use with common reference EEG
       data. Use with other types of data are at your own risk.


    Parameters
    ----------
    epochs_df : pd.DataFrame
        must have epoch_id and time row index names
   
    eeg_streams : list-like of str
        the names of colums to transform
       
    ref : str or list-like of str
        name of the 2nd stream for a linked pair, the new common
        reference, or the complete list of streams to use for a common
        average reference
        
    type : str = {'linked_pair', 'new_common', 'common_average'}

    epoch_id : str, optional

    time : str, optional


    Returns
    -------
    pd.DataFrame
       a copy of epochs_df with `eeg_streams` re-referenced


    Note
    ----

    `linked_pair`
       Transforms the EEG data to a "linked" pair reference:

       .. math::
          EEG_{\\text{re-referenced}} = EEG - (0.5 \\times EEG_{ref})

       May be used to switch from an A1 left mastoid common reference to a
       common linked A1, A2 mastoid reference ("bimastoid").

    `new_common`
        Transforms EEG to a different common reference location:
    
        .. math::
           EEG_{\\text{re-referenced}} = EEG - EEG_{ref}

        May be used switch from an A1 common reference to a vertex or
        nose-tip reference.

    `common_average`
        Transforms EEG to a common average reference of :math:`N` EEG reference streams

        .. math::
           EEG_{\\text{re-referenced}} = EEG - \\frac{\\sum_{i=0}^{i=N}{EEG_{ref[i]}}}{N}


   
    Examples
    --------

    Switch from A1 reference to linked-mastoids

    >>> eeg_streams = ['MiPf', 'MiCe', 'MiPa', 'MiOc']
    >>> re_reference(epochs_df, eeg_streams, 'A2', 'linked_pair')

    
    Switch to a vertex reference, MiCe

    >>> eeg_streams = ['MiPf', 'MiCe', 'MiPa', 'MiOc']  
    >>> br_epochs_df = epf.re_reference(epochs_df, eeg_streams, 'MiCe', "new_common")


    Switch to a common average reference (typically all available EEG data streams)

    >>> eeg_streams = ['MiPf', 'MiCe', 'MiPa', 'MiOc']  
    >>> ref = eeg_streams
    >>> br_epochs_df = epf.re_reference(epochs_df, eeg_streams, ref, "common_average")

    """

    _epochs_QC(epochs_df, eeg_streams, epoch_id=epoch_id, time=time)

    # ref must be a list of strings with len(ref)>1 for ref_type of 'common_average'
    if ref_type == "common_average":
        if not (isinstance(ref, list) and len(ref) > 1) or not all(
            isinstance(item, str) for item in ref
        ):
            raise ValueError(
                "ref should be a list of strings with length greater than 1."
            )

    if isinstance(ref, list) and len(ref) == 1:
        ref = "".join(ref)

    if ref_type == "linked_pair":
        new_ref = epochs_df[ref] / 2.0
    elif ref_type == "new_common":
        new_ref = epochs_df[ref]
    elif ref_type == "common_average":
        new_ref = epochs_df[ref].mean(axis=1)
    else:
        raise ValueError(f"unknown reference type: ref_type={ref_type}")

    br_epochs_df = epochs_df.copy()
    for col in eeg_streams:
        br_epochs_df[col] = br_epochs_df[col] - new_ref

    return br_epochs_df


def fir_filter_epochs(
    epochs_df,
    data_columns,
    ftype=None,
    cutoff_hz=None,
    width_hz=None,
    ripple_db=None,
    window=None,
    sfreq=None,
    trim_edges=False,
    epoch_id=EPOCH_ID,
    time=TIME,
):
    """apply FIRLS filtering to spudtr format epoched data

    Parameters
    ----------
    epochs_df : pd.DataFrame 
        must be a spudtr format epochs dataframe with epoch_id, time columns
    data_columns: list of str
        column names to apply the transform
    ftype : str {'lowpass' , 'highpass', 'bandpass', 'bandstop'}
        filter type
    cutoff_hz : float or 1D-array-like of floats, length 2
        1/2 amplitude cutoff frequency in Hz
    width_hz : float
        pass-to-stop transition band width (Hz), symmetric for bandpass, bandstop
    ripple_db : float
        ripple, in dB, e.g., 53.0, 60.0
    window : str {'kaiser','hamming','hann','blackman'}
        window type for firwin
    sfreq : float
        sampling frequency, e.g., 250.0, 500.0
    trim_edges : bool
        True trim edges, False not trim edges
    epoch_id : str {"epoch_id"}, optional
        column name for epoch index
    time: str {"time"}, optional
        column name for timestamps

    Returns
    -------
    pd.DataFrame
        a copy of epochs_df, with data in `data_columns` filtered


    Notes
    -----
    All the filter parameters are mandatory, consider making a
    ``filter_params`` dictionary and expanding it like so
    ``fir_filter_epochs( ..., **filter_params)``.

    By default the filtered epochs have the same length as the
    original. The `trim_edges` option returns the center interval of
    each epoch, free from distortion at the edges but this may result in
    considerable data loss depending on the filter specifications.


    Examples
    --------
    >>> ftype = "bandpass"
    >>> cutoff_hz = [18, 35]
    >>> sfreq = 250
    >>> window = "kaiser"
    >>> width_hz = 5
    >>> ripple_db = 60
    >>> epoch_id = "epoch_id"
    >>> time = "time_ms"
    >>> filt_test_df = epochs_filters(
            epochs_df, 
            data_columns,
            ftype=ftype,
            cutoff_hz=cutoff_hz,
            width_hz=width_hz,
            ripple_db=ripple_db,
            window=window,
            sfreq=sfreq,
            trim_edges=False
            epoch_id=epoch_id
            time=time
    )

    """

    # it is crucial to enforce the spudtr epochs format because trimming
    # needs to know about epoch boundaries and times
    _epochs_QC(epochs_df, data_columns, epoch_id=epoch_id, time=time)

    _fparams = dict(
        ftype=ftype,
        cutoff_hz=cutoff_hz,
        sfreq=sfreq,
        width_hz=width_hz,
        ripple_db=ripple_db,
        window=window,
    )

    # build and apply the filter
    filt_epochs_df = fir_filter_dt(epochs_df, data_columns, **_fparams)

    # this trims edges in *each epoch*, 1/2 length of the filter
    if trim_edges:
        taps = _design_firwin_filter(**_fparams)
        n_edge = int(np.floor(len(taps) / 2.0))
        times = filt_epochs_df[time].unique()
        start_good = times[n_edge]  # first good sample
        stop_good = times[-(n_edge + 1)]  # last good sample
        qstr = f"{time} >= @start_good and {time} <= @stop_good"
        filt_epochs_df = filt_epochs_df.query(qstr).copy()

    return filt_epochs_df
