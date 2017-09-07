#!/usr/bin/python3
# simple example of stereo panner with pygame
# some code modified from http://soundrts.blogspot.com/2008/01/some-pygame-examples-for-audiogame.html
# 9/6/17

import pygame


filepath = '/home/pi/pnnr/sound/test/alex_NE_100_44.wav'
time = pygame.time
mixer = pygame.mixer

mixer.init(frequency=44100)
sound = mixer.Sound(filepath)
sound.set_volume(0.4)  # lower sound's overall volume

channel = sound.play(loops=-1)  # loop indefinitely

channel.set_volume(1, 0)  # pan to the left
time.delay(1000)
channel.set_volume(0, 1)  # pan to the right
time.delay(1000)
channel.set_volume(1, 1)  # full stereo
time.delay(1000)

channel.stop()  # stop the indefinite loop
