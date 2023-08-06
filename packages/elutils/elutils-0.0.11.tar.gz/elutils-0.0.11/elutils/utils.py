"""Various misc utils that do not fit elsewhere"""
from collections import Counter
from collections.abc import Iterable
from datetime import datetime

# COUNTER
def inf_counter(start_num=0):
    """An infinite incremental counter"""
    while True:
        start_num+=1
        yield start_num

# DICT INTERFACE
def sum_dicts(dicts:Iterable):
    """takes a list of dicts as input and returns one dict with all values summed togeher"""

    if len(dicts)==0:
        return {}

    counter_dicts = [Counter(d) for d in dicts]

    result_dict = counter_dicts[0]
    for d in counter_dicts[1:]:
        result_dict += d
    return result_dict

# TIME
def current_time(sep='-'):
    """Returns the current time as HH-MM-SS format
    can specify the separator between times, default to -"""
    now = datetime.now()
    current_time = now.strftime(f"%H{sep}%M{sep}%S")
    return current_time


def epoch_to_datetime(epoch_time,fmt=None,utc=True):
    """If fmt is provided it returns a string, otherwise datetime object"""
    if utc:
        # utc
        converted = datetime.utcfromtimestamp(epoch_time)
    else:
        # local time
        converted = datetime.fromtimestamp(epoch_time)

    if fmt is None:
        return converted
    else:
        return datetime.strftime(converted,fmt)
