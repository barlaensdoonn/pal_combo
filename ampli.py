#!/usr/bin/python3
# MAX9744 utility methods
# 9/7/17
# updated: 9/7/17

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
    '''wrapper for adafruit's MAX9744 class'''

    def __init__(self, volume=16):
        self.mute = 0
        self.max = 63
        self.volume = volume
        self.amp = MAX9744()
        self.amp.set_volume(self.volume)

    def set_volume(self, volume):
        '''value should be between 0-63 inclusive'''

        print('received request to set volume to {}'.format(volume))
        volume = self.mute if volume < self.mute else self.max if volume > self.max else volume
        self.volume = volume

        print('setting volume to {}...'.format(volume))
        self.amp.set_volume(volume)

    def decrease_volume(self):
        print('decreasing volume by one step')
        self.amp.decrease_volume()

    def increase_volume(self):
        print('increasing volume by one step')
        self.amp.increase_volume()

    def ramp_up(self):
        volume = self.volume
        interval = self.max - volume

        if not interval:
            print('already at max volume')
            return

        try:
            for i in range(interval):
                volume += 1
                self.set_volume(volume)
                time.sleep(1)
        except KeyboardInterrupt:
            print('user interrupt received')
            print('leaving volume set to {}'.format(self.volume))
