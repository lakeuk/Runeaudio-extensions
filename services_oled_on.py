#!/usr/bin/env python2
import os
os.system("cp /home/myapp/oledRuneaudio.service /usr/lib/systemd/system")
os.system("systemctl start oledRuneaudio")
os.system("systemctl enable oledRuneaudio")