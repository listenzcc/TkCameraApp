'''
File: myTimer.py
Author: Chuncheng
Version: 0.0
Purpose: High Precision MilliSeconds Level Timer
'''

import time


class MyTimer(object):
    ''' The Timer object of High Precision MilliSeconds Level Timer.
    '''

    def __init__(self):
        pass

    def hp_sleep(self, interval):
        '''
        Sleep for [interval] seconds in high precision.
        Be ware, it is very CPU consuming.

        Args:
        - @interval: The interval to sleep.

        Outputs:
        - The time has been passed, in Seconds.
        '''
        t = time.time()
        if interval < 0:
            print('W: Interval is negative, can not sleep for that long.')
        else:
            stop = t + interval
            while True:
                if stop - time.time() > 0.03:
                    time.sleep(0.001)
                if not time.time() < stop:
                    break
        d = time.time() - t
        return d
