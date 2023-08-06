"""
A set of methods for manipulating interval data.
These methods deal with interval dataframes which must be indexed with a Pandas DatetimeIndex
or float (seconds since Epoch).
Different methods are provided for interval dataframes marked EoI (end-of-interval) vs. BoI (beginning-of-interval).

Author: J. M. Fife
"""

import pandas as pd
import numpy as np
import math
import datetime


def mark_gaps_eoi(input_interval_df, tolerance_factor=0.1):
    """
    Insert rows with numpy.nan as necessary in an interval dataframe to mark gaps
    Expects an interval dataframe.
    By interval dataframe, it means a dataframe where the values timestamped represent the average values
    over the time interval.
    This method works for EoI-timestamped interval dataframes.
    Args:
        input_interval_df: an indexed Pandas interval DataFrame (where values are averages over previous interval)
        tolerance_factor: factor to be multiplied by the expected time interval and used for checking for missing data
    Returns:
        a Pandas DataFrame with new records for any gap containing values numpy.nan
    """
    interval_df = input_interval_df.copy()
    if isinstance(input_interval_df, pd.DataFrame):
        t_array = input_interval_df.index
        if not (isinstance(t_array, pd.DatetimeIndex) or (t_array.dtype == float)):
            raise TypeError('index must be a Pandas DatetimeIndex or float')
        cols = input_interval_df.columns
    else:
        raise TypeError("accepts only a Pandas DataFrame")
    dt_observed = [(t_array[i] - t_array[i - 1]) for i in range(1, len(interval_df))]
    if 'interval_duration' in cols:
        # this data has a field that represents the duration of each record
        if isinstance(t_array, pd.DatetimeIndex):
            dt_expected = pd.to_timedelta(interval_df['interval_duration'].values, unit="sec")[1:]
        else:
            dt_expected = interval_df['interval_duration'].values[1:]
        # Check each interval for consistency and if not consistent, append a new record
        for i in range(len(dt_observed)):
            if (dt_observed[i] - dt_expected[i]) > dt_expected[i] * tolerance_factor:
                interval_df = interval_df.append(pd.DataFrame(index=[t_array[i + 1] - dt_expected[i]]))
    else:
        # expected interval length is set to median of the actual observed times between interval records
        dt_expected = np.quantile(dt_observed, 0.5, interpolation='lower')
        # Check each interval for consistency and if not consistent, append a new record
        for i in range(len(dt_observed)):
            if (dt_observed[i] - dt_expected) > dt_expected * tolerance_factor:
                if isinstance(t_array, pd.DatetimeIndex):
                    interval_df = interval_df.append(
                        pd.DataFrame(index=pd.DatetimeIndex([t_array[i + 1] - dt_expected])))
                else:
                    interval_df = interval_df.append(pd.DataFrame(index=[t_array[i + 1] - dt_expected]))
    interval_df.sort_index(inplace=True)
    return interval_df


def mark_gaps_boi(input_interval_df, tolerance_factor=0.1):
    """
    Insert rows with numpy.nan as necessary in an interval dataframe to mark gaps
    Expects an interval dataframe.
    By interval dataframe, it means a dataframe where the values timestamped represent the average values
    over the time interval.
    This method works for BoI-timestamped.
    Args:
        input_interval_df: an indexed Pandas interval DataFrame (where values are averages over previous interval)
        tolerance_factor: factor to be multiplied by the expected time interval and used for checking for missing data
    Returns:
        a Pandas DataFrame with new records for any gap containing values numpy.nan
    """
    interval_df = input_interval_df.copy()
    if isinstance(input_interval_df, pd.DataFrame):
        t_array = input_interval_df.index
        if not (isinstance(t_array, pd.DatetimeIndex) or (t_array.dtype == float)):
            raise TypeError('index must be a Pandas DatetimeIndex or float')
        cols = input_interval_df.columns
    else:
        raise TypeError("accepts only a Pandas DataFrame")
    dt_observed = [(t_array[i] - t_array[i - 1]) for i in range(1, len(interval_df))]
    if 'interval_duration' in cols:
        # this data has a field that represents the duration of each record
        if isinstance(t_array, pd.DatetimeIndex):
            dt_expected = pd.to_timedelta(interval_df['interval_duration'].values, unit="sec")[1:]
        else:
            dt_expected = interval_df['interval_duration'].values[1:]
        # Check each interval for consistency and if not consistent, append a new record
        for i in range(len(dt_observed)):
            if (dt_observed[i] - dt_expected[i]) > dt_expected[i] * tolerance_factor:
                interval_df = interval_df.append(pd.DataFrame(index=[t_array[i + 1] - dt_expected[i]]))
    else:
        # expected interval length is set to median of the actual observed times between interval records
        dt_expected = np.quantile(dt_observed, 0.5, interpolation='lower')
        # Check each interval for consistency and if not consistent, append a new record
        for i in range(len(dt_observed)):
            if (dt_observed[i] - dt_expected) > dt_expected * tolerance_factor:
                if isinstance(t_array, pd.DatetimeIndex):
                    interval_df = interval_df.append(pd.DataFrame(index=pd.DatetimeIndex([t_array[i] + dt_expected])))
                else:
                    interval_df = interval_df.append(pd.DataFrame(index=[t_array[i] + dt_expected]))
    interval_df.sort_index(inplace=True)
    return interval_df


def to_interval_series_uniform_eoi(series_interval_nonuniform, freq: str = '15min'):
    """
    Convert a pandas interval Series with a DatetimeIndex into a uniformly time-sampled Series.
    Be interval Series, it means a pandas Series where the values timestamped represent the average values
    over the previous time interval (from the previous timestamp to the present one). Pandas resample()
    methods does not have the ability to handle this case to my knowledge.
    Args:
        series_interval_nonuniform: the raw pandas DataFrame to convert -- must be indexed with DatetimeIndex
        freq: frequency specifier from pandas

    Returns:
        A resampled Series
    """
    # First create the desired list of uniform datetimes and incorporate them into the original nonuniform series
    index_min = min(series_interval_nonuniform.index).ceil(freq=freq)
    index_max = max(series_interval_nonuniform.index).floor(freq=freq)
    series_interval_nonuniform_2 = series_interval_nonuniform.copy()
    uniform_index = pd.date_range(start=index_min, end=index_max, freq=freq)
    for index in uniform_index:
        series_interval_nonuniform_2.loc[index] = \
            series_interval_nonuniform.iloc[series_interval_nonuniform.index.get_loc(index, method='backfill')]
    series_interval_nonuniform_2.sort_index(inplace=True)
    # Now we have a modified nonuniform series with row corresponding to each uniform time point
    # loop through them and assign the intervals to the appropriate bin
    series_interval_uniform = pd.Series(np.zeros(len(uniform_index)), index=uniform_index)
    lastindex = series_interval_nonuniform_2.index[0]
    max_i_uniform = len(series_interval_uniform) - 1
    for index, val in series_interval_nonuniform_2.items():
        index_float = (index - series_interval_uniform.index[0]) / series_interval_uniform.index.freq
        i_uniform = math.ceil(index_float)
        if 0 < i_uniform <= max_i_uniform:
            frac = (index - lastindex) / series_interval_uniform.index.freq
            series_interval_uniform.iloc[i_uniform] += val * frac
        lastindex = index
    return series_interval_uniform


def to_plottable_interval_timeseries_eoi(input_interval_series):
    """
    Convert an interval series to something that is more plottable by adding points to the LHS of each interval.
    Args:
        input_interval_series: a series of intervals (assumes floating point values are averages over previous interval)

    Returns:
        an (x_array, y_array) tuple
    """
    if isinstance(input_interval_series, pd.Series):
        t = input_interval_series.index
        y = input_interval_series.values
    else:
        if isinstance(input_interval_series, tuple):
            t = input_interval_series[0]
            y = input_interval_series[1]
        else:
            raise TypeError("accepts only a Pandas Series or (t_array, y_array) tuple")
    t_new = [k for rept in t for k in (rept, rept)]
    y_new = [k for rept in y for k in (rept, rept)]
    t_new = t_new[1:-1]
    y_new = y_new[2:]
    return t_new, y_new


def to_plottable_interval_vectors_boi(input_interval_series):
    """
    Convert an interval series to something that is more plottable by adding points to the RHS of each interval.
    Assumes the input interval series is completely populated, and takes the time between the last two intervals
    as the interval duration (for efficiency)
    Args:
        input_interval_series: a series of intervals (assumes floating point values are averages over subsequent
            interval)

    Returns:
        an (x_array, y_array) tuple
    """
    if isinstance(input_interval_series, pd.Series):
        t = input_interval_series.index
        y = input_interval_series.values
    else:
        if isinstance(input_interval_series, tuple):
            t = input_interval_series[0]
            y = input_interval_series[1]
        else:
            raise TypeError("accepts only a Pandas Series or (t_array, y_array) tuple")
    if len(t) > 1:
        # calculate the interval duration
        dt = t[-1] - t[-2]
        t_new = [k for rept in t for k in (rept, rept)]
        y_new = [k for rept in y for k in (rept, rept)]
        t_new = t_new[1:]
        t_new.append(t[-1] + dt)
        return t_new, y_new
    else:
        raise TypeError("number of elements in the series must be > 1")


def to_plottable_interval_timeseries_boi(input_interval_series):
    """
    Convert an interval series to something that is more plottable by adding points to the RHS of each interval.
    Assumes the input interval series is completely populated, and takes the time between the last two intervals
    as the interval duration (for efficiency)
    Args:
        input_interval_series: a series of intervals (assumes floating point values are averages over subsequent
            interval)

    Returns:
        a Pandas series
    """
    (t_new, y_new) = to_plottable_interval_vectors_boi(input_interval_series)
    series_new = pd.Series(y_new, index=t_new)
    return series_new
