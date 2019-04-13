#!/usr/bin/env python2

import os

os.system("systemctl disable ePaperRuneaudio")

os.system("systemctl stop ePaperRuneaudio")

os.system("rm /usr/lib/systemd/system/ePaperRuneaudio.service")
