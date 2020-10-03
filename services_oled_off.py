#!/usr/bin/env python2
import os
os.system("systemctl disable oledRuneaudio")
os.system("systemctl stop oledRuneaudio")
os.system("rm /usr/lib/systemd/system/oledRuneaudio.service")
