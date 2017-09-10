#!/usr/bin/python3
# MAX9744 library wrapper
# 9/7/17
# updated: 9/9/17

import time
from Adafruit_MAX9744 import MAX9744


class Ampli(object):
    '''
    wrapper for adafruit's MAX9744 library, which has following methods:
    set_volume(), increase_volume(), decrease_volume()
    if controlling more than one amp from a single pi, must change
    the i2c address on the amp itself and pass in new address to MAX9744()
    more here: https://github.com/adafruit/Adafruit_Python_MAX9744
    '''

    def __init__(self, volume=16):
        self.min = 0
        self.max = 63
        self.volume = volume
        self.unmute_volume = self.volume
        self.amp = MAX9744()
        self.set_volume(self.volume)

    def _constrain(self, value):
        '''valid values are 0-63 inclusive'''
        cnstrnd = self.min if value < self.min else self.max if value > self.max else value

        if cnstrnd != value:
            print('received value of {} outside valid range of 0-63'.format(value))
            print('constraining to {}'.format(cnstrnd))

        return cnstrnd

    def set_volume(self, value, suppress=False):
        '''valid values are 0-63 inclusive'''
        value = self._constrain(value)

        if not suppress:
            print('setting volume to {}...'.format(value))

        self.amp.set_volume(value)
        self.volume = value

    def decrease_volume(self):
        self.amp.decrease_volume()
        self.volume -= 1
        print('decreased volume by one step to {}'.format(self.volume))

    def increase_volume(self):
        self.amp.increase_volume()
        self.volume += 1
        print('increased volume by one step to {}'.format(self.volume))

    def mute(self):
        print('muting amp')
        self.unmute_volume = self.volume
        self.set_volume(self.min, suppress=True)

    def unmute(self):
        print('unmuting amp')
        self.set_volume(self.unmute_volume, suppress=True)

    def ramp_to(self, value):
        '''
        ramp from current volume to input value by one step in one second increments.
        use Ctrl-C to interrupt the process and leave volume set to the current step
        '''
        direction = None
        target = self._constrain(value)

        if target == self.volume:
            print('volume already set to {}'.format(target))
            return
        elif target > self.volume:
            direction = 1
            interval = target - self.volume
        elif target < self.volume:
            direction = -1
            interval = self.volume - target

        try:
            print('ramping volume from {} to {} in 1 second increments'.format(self.volume, target))
            step = self.volume
            for i in range(interval):
                step += direction
                self.set_volume(step)
                time.sleep(1)
        except KeyboardInterrupt:
            print('\nuser interrupt received')
            print('leaving volume set to {}'.format(self.volume))
