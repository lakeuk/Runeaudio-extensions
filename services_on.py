#!/usr/bin/env python2

import os

os.system("cp /home/myapp/ePaperRuneaudio.service /usr/lib/systemd/system")
os.system("cp /home/myapp/gpioRuneaudioi2c.service /usr/lib/systemd/system")
os.system("cp /home/myapp/gpioRuneaudioi2cRotary.service /usr/lib/systemd/system")
os.system("cp /home/myapp/oledRuneaudio.service /usr/lib/systemd/system")

os.system("systemctl start gpioRuneaudioi2c")
os.system("systemctl start gpioRuneaudioi2cRotary")
os.system("systemctl start ePaperRuneaudio")
os.system("systemctl start oledRuneaudio")

os.system("systemctl enable gpioRuneaudioi2c")
os.system("systemctl enable gpioRuneaudioi2cRotary")
os.system("systemctl enable ePaperRuneaudio")
os.system("systemctl enable oledRuneaudio")
