#!/usr/bin/python3
# simple example of stereo panner with pygame
# some code modified from http://soundrts.blogspot.com/2008/01/some-pygame-examples-for-audiogame.html
# 9/6/17
# updated 9/10/17

import os
from pygame import mixer
from pygame import time as pytime


prefix = '/home/pi/pal_combo/ignore/sound/alex'
files = [
    'alex_NE_100_44.wav',
    'alex_VER_100_44.wav',
    'alex_ODD_100_44.wav',
    'alex_OR_100_44.wav',
    'alex_EV_100_44.wav',
    'alex_EN_100_44.wav'
]

filepaths = [os.path.join(prefix, files[i]) for i in range(len(files))]
sounds = [mixer.Sound(filepath) for filepath in filepaths]
left = (1, 0)
right = (0, 1)
mixer.init(frequency=44100, buffer=1024)  # default buffer is 4096


def wait(channel):
    '''
    pause until channel is done playing sound. using this technique results
    in noticeable gaps between the end of one sound and start of next.
    calculate_waits technique takes this into account
    '''
    while channel.get_busy():
        pass


def calculate_waits(sounds):
    '''return list of wait times in ms calculated as length of sound - 100ms'''

    lngths = []
    for i in range(len(sounds)):
        lngth = sounds[i].get_length()
        lngth = lngth * 1000 - 100
        lngths.append(int(lngth))

    return lngths


def loop_by_length(sounds):
    waits = calculate_waits(sounds)
    clock = pytime.Clock()

    for i in range(len(sounds)):
        clock.tick()
        channel = mixer.find_channel()

        if not i % 2:
            channel.set_volume(*left)
        else:
            channel.set_volume(*right)

        channel.play(sounds[i])
        pytime.wait(waits[i])
        # channel.stop()
        print(clock.get_time())
