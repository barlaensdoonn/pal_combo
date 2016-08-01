#!/usr/bin/python3
# code for floaters
# 7/31/16

import random
from Adafruit_MAX9744 import MAX9744

# ## amplings ## #
volume = 32
amp = MAX9744()

# ## palindrome variables ## #
palindrome = ["NE", "VER", "ODD", "OR", "EV", "EN"]
# palindrome = ["BA", "NA", "NA"]
syllable_dict = dict(enumerate(palindrome))
voices_num = int(input("How many voices will speak each syllable? "))
iter_num = int(input("How many times would you like the palindrome spoken?  "))
syllable_num = len(palindrome)

# changed to list comp for python3
voices = [x for x in range(1, voices_num + 1)]

# create iteration list of voice_dicts
iter_list = []


def set_gain(volume):
    amp.set_volume(volume)


def shuffleACopy(x):
    b = x[:]  # make a copy of the keys
    random.shuffle(b)  # shuffle the copy
    return b  # return the copy


for i in range(iter_num):
    # make shuffled copies of the voices list for each syllable
    voices_list = [shuffleACopy(voices) for x in range(syllable_num)]
    # voice_dict is made using a shortcut, but should use keys from
    # syllable_dict rather than enumerate
    # voice_dict = dict(enumerate(voices_list))  # dictionary of one iteration

    # this uses syllable_dict keys but results in the same thing because
    # the length of voices_list is dependent on syllable_num:
    voice_dict = {x: voices_list[x] for x in list(syllable_dict.keys())}

    # depending on what you want the keys to be
    # iter_dict = {value : voice_dict.get(key, None) for key, value in syllable_dict.items()}
    # iter_list.append(iter_dict)
    iter_list.append(voice_dict)


# output of syllable id and voice id pairs until voice exhaustion and
# then moves to next iteration
for i in iter_list:
    for x in range(voices_num):
        # changed to .items() for python3
        for key, value in i.items():
            print("syllable: {}, voice: {}".format(syllable_dict[key], value[x]))


# if we want it as a list:
[[k, d[k][i]] for d in iter_list for i in range(voices_num) for k in sorted(d)]
