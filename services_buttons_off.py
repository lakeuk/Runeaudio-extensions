#!/usr/bin/env python2

import os

os.system("systemctl disable gpioRuneaudioi2c")
os.system("systemctl disable gpioRuneaudioi2cRotary")

os.system("systemctl stop gpioRuneaudioi2c")
os.system("systemctl stop gpioRuneaudioi2cRotary")

os.system("rm /usr/lib/systemd/system/gpioRuneaudioi2c.service")
os.system("rm /usr/lib/systemd/system/gpioRuneaudioi2cRotary.service")

