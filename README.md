# pal_combo
1. Unit of observation is a syllable in the palindrome, NE-VER-ODD-OR-EV-EN
2. For each syllable in the palindrome, we want x different voices to pronounce it
3. We will loop through the sets of syllables, always starting with the first (NE) and ending with the last (EN), and randomly choose a voice from the set of x voices, without repeating a voice until all options have been exhausted
4. We will repeat this process y times


## components
each component below represents its own module
(server and clients are raspberry pis)


#### *combinatorics*
iterate pairwise through 2 sets of variables without repeating combinations, explained above


#### *server-client communication via sockets*
use UDP sockets to broadcast messages to listening clients
* each client controls 2 channels of audio
* each channel of audio corresponds to a specific voice
* a single server will run the combinatorics code and broadcast a message across the local network signifying the current combination
* audio will be triggered on listening clients if the message corresponds to their voice


#### *use pygame and stereo panning to play specific audio file*
trigger playback of audio file based on received command
* command - file correlated via dictionary
* utilize stereo panning to isolate client's audio channels

#### *control amp hardware via I2C*
interface via client's GPIO with Adafruit's [MAX9744 amplifier](https://learn.adafruit.com/adafruit-20w-stereo-audio-amplifier-class-d-max9744/overview) using their supplied library


## install notes

#### *MAX9744 amp library and dependencies*
```
sudo apt-get install python-smbus
git clone https://github.com/adafruit/Adafruit_Python_MAX9744.git
cd Adafruit_Python_MAX9744
sudo python3 setup.py install
```
enable I2C in raspi-config

#### *pygame and dependencies*
```
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
sudo pip3 install pygame
```
reference: https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=33157&p=332140&hilit=croston%2bpygame#p284266

- or - (untested)

```
sudo apt-get install python3-pygame
```
