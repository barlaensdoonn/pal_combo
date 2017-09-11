#!/usr/bin/python3
# simple example of stereo panner with pygame
# some code modified from http://soundrts.blogspot.com/2008/01/some-pygame-examples-for-audiogame.html
# 9/6/17
# updated 9/10/17

import os
from pygame import mixer
from pygame import time as pytime


class Panner(object):

    search_path = '/home/pi/pal_combo/ignore/sound/alex'

    def __init__(self, soundpath=search_path):
        self.pan_left = (1, 0)
        self.pan_right = (0, 1)
        self.mixer = mixer
        self.mixer.init(frequency=44100, buffer=1024)  # default buffer is 4096
        self._init_sounds(soundpath)
        self.waits = self._calculate_waits()

    def _init_sounds(self, soundpath):
        filepaths = []

        for dirpath, dirnames, filenames in os.walk(soundpath):
            for thing in filenames:
                filepaths.append(os.path.join(dirpath, thing))

        self.sounds = [self.mixer.Sound(filepath) for filepath in filepaths]

    def _wait(self, channel):
        '''
        pause until channel is done playing sound.
        using this technique results in noticeable gaps between the end of one sound and start of next.
        calculate_waits technique takes this into account, use that instead.
        '''
        while channel.get_busy():
            pass

    def _calculate_waits(self):
        '''return list of wait times in ms calculated as length of sound - 100ms'''

        lngths = []
        for i in range(len(self.sounds)):
            lngth = self.sounds[i].get_length()
            lngth = lngth * 1000 - 100
            lngths.append(int(lngth))

        return lngths

    def loop_once(self):
        clock = pytime.Clock()

        for i in range(len(self.sounds)):
            clock.tick()
            channel = self.mixer.find_channel()

            if not i % 2:
                channel.set_volume(*self.pan_left)
            else:
                channel.set_volume(*self.pan_right)

            channel.play(self.sounds[i])
            self.wait(channel)
            # pytime.wait(self.waits[i])
            # channel.stop()
            print(clock.get_time())
