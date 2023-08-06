"""Various tools useful for testing stuff"""
import time
from typing import Callable


def wait_for_event(event,timeout=None):
    ''''''
    event.wait(timeout=timeout)



def wait_for_expression_to_be_true(expression:Callable,timeout):
    time_waited=0

    while not expression():

        print(str(time.time())[-1])

        time.sleep(0.01)
        time_waited+=0.01
        if time_waited>timeout:
            raise TimeoutError




if __name__ == '__main__':

    try:
        wait_for_expression_to_be_true(lambda :str(time.time())[-1]=='8',timeout=25)
        print('Expression was true')
    except TimeoutError:
        print("Timed out")
