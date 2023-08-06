"""Contains all decorators used. Timeit primarily used performance optimization and debugging."""
import time
import random
import functools
from functools import wraps
import datetime
import pickle
import os
import threading

def timeit(method):
    """Decorator for measuring how much time a func took to run"""
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' %  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def retry(tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    msg = f"{e}, Retrying in {mdelay} seconds..."
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

def cache_decayable_data(data_expires_after: datetime.timedelta, DECAYABLE_DATA_LOCATION: str= "buffered_data",verbose=False):
    """Buffers data that gets outdated after a while, uses buffered data if it is still valid.
    Unless DECAYABLE_FILES_LOCATION is specified in the environment it saves the data as a pickle
    file in same location module where the decorated function was in. Recommend to set to reduce clutter.
    :param data_expires_after a timedelta of how long it takes the data to become outdated
    :param DECAYABLE_DATA_LOCATION what option in the enviroment to lookup to get the location to save the buffered data
    :param the decorated function must return the data to be saved
    :param verbose bool,
    """
    def cache_decayable_data_decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            decayable_files_location = os.environ.get(DECAYABLE_DATA_LOCATION, "")
            decayable_file_path = os.path.join(decayable_files_location,f'{func.__name__}{"_args_" if len(args)>0 else""}{"-".join([*args])}{"_kwargs_" if len(kwargs)>0 else ""}{"-".join(kwargs.values())}.decay.p')
            try:
                with open(decayable_file_path,'rb') as file:
                    expiry,data = pickle.load(file)
                    # data is expired
                    if datetime.datetime.now() >= expiry:
                        if verbose:
                            print(f"{func.__name__} cache has expired")
                        data = func(*args,**kwargs)
                        # save data
                        with open(decayable_file_path, 'wb') as file:
                            expiry_date = datetime.datetime.now() + data_expires_after
                            pickle.dump((expiry_date, data), file)
                        return data
                    # data can still be used, return as is
                    else:
                        if verbose:
                            print(f"{func.__name__} cache is valid, using cached data.")

                        return data

            except Exception as e:
                data = func(*args,**kwargs)
                # save data
                with open(decayable_file_path,'wb') as file:
                    expiry_date = datetime.datetime.now() + data_expires_after
                    pickle.dump((expiry_date,data),file)
                return data
        return wrapper
    return cache_decayable_data_decorator

def run_function_in_thread_on_event(func, event, *args, **kwargs):
    """Start a new thread that waits until {event} is true, then runs {func}
    :param func: the function to execute
    :param event: the event that will trigger func to fun
    :param args kwargs: Arguments for func"""
    def wait_for_event(func):
        @wraps(func)
        def wrapper(event):
            event.wait()
            func()
        return wrapper
    partial_func = functools.partial(func,*args,**kwargs)
    decorated_partial_func = wait_for_event(partial_func)
    t = threading.Thread(target=decorated_partial_func,args=(event,),name=func.__name__)
    t.start()
