#!/usr/bin/python3
# MAX9744 utility methods
# 9/7/17
# updated: 9/9/17

# ## NOTES ## #
# must install Adafruit's MAX9744 python library
# more here: https://github.com/adafruit/Adafruit_Python_MAX9744

# Create a MAX9744 class instance.  With no arguments to the initializer it will
# pick a default I2C bus and device address to look for the MAX9744.
# On a Raspberry Pi connect the MAX9744 SCL and SDA pins to the Pi GPIO header
# SCL and SDA pins.  Make sure I2C has been enabled too, see:
#  https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/config$
# On a BeagleBone Black the default I2C bus is /dev/i2c-1 which is exposed on
# SCL pin P9_19 and SDA pin P9_20. The next line instantiates the class:
# amp = MAX9744()

# Alternatively you can specify the I2C bus and/or device address by providing
# optional parameter values:
# amp = MAX9744(busnum=2, address=0x4C)
# ## END NOTES ## #

import time
from Adafruit_MAX9744 import MAX9744


class Ampli(object):
    '''wrapper for adafruit's MAX9744 library'''

    def __init__(self, volume=16):
        self.mute = 0
        self.max = 63
        self.volume = volume
        self.amp = MAX9744()
        self.set_volume(self.volume)

    def _constrain(self, value):
        '''valid values are 0-63 inclusive'''
        cnstrnd = self.mute if value < self.mute else self.max if value > self.max else value

        if cnstrnd != value:
            print('received value of {} outside valid range of 0-63'.format(value))
            print('constraining to {}'.format(cnstrnd))

        return cnstrnd

    def set_volume(self, value):
        '''valid values are 0-63 inclusive'''
        value = self._constrain(value)

        print('setting volume to {}...'.format(value))
        self.amp.set_volume(value)
        self.volume = value

    def decrease_volume(self):
        print('decreasing volume by one step')
        self.amp.decrease_volume()

    def increase_volume(self):
        print('increasing volume by one step')
        self.amp.increase_volume()

    def mute(self):
        self.set_volume(self.mute)

    def ramp_to(self, value):
        '''
        ramp from current volume to imput value by one step in one second increments.
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
