import datetime
import math


_GPS_TIME_START = datetime.datetime(1980, 1, 6, 0, 0, 0)

# ------------------------------------------------------------------------------


def weektow_to_datetime(tow, week):

    delta = datetime.timedelta(weeks=week, seconds=tow)

    return _GPS_TIME_START + delta


def epoch_range(start_epoch, end_epoch, interval_s):
    """
    Iterate between 2 epochs with a given interval

    >>> import datetime
    >>> st = datetime.datetime(2015, 10, 1,  0,  0,  0)
    >>> en = datetime.datetime(2015, 10, 1,  0, 59, 59)
    >>> interval_s = 15 * 60
    >>> ','.join([str(d) for d in epoch_range(st, en, interval_s)])
    '2015-10-01 00:00:00,2015-10-01 00:15:00,2015-10-01 00:30:00,2015-10-01 00:45:00'
    >>> st = datetime.datetime(2015, 10, 1,  0,  0,  0)
    >>> en = datetime.datetime(2015, 10, 1,  1,  0,  0)
    >>> interval_s = 15 * 60
    >>> ','.join([str(d) for d in epoch_range(st, en, interval_s)])
    '2015-10-01 00:00:00,2015-10-01 00:15:00,2015-10-01 00:30:00,2015-10-01 00:45:00,2015-10-01 01:00:00'
    """

    total_seconds = (end_epoch - start_epoch).total_seconds() + interval_s / 2.0
    n_intervals_as_float = total_seconds / interval_s
    n_intervals = int(n_intervals_as_float)
    if math.fabs(n_intervals - n_intervals_as_float) >= 0.5:
        n_intervals = n_intervals + 1

    for q in range(n_intervals):
        yield start_epoch + datetime.timedelta(seconds=interval_s * q)



