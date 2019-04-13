#!/usr/bin/env python2

import os

os.system("cp /home/myapp/ePaperRuneaudio.service /usr/lib/systemd/system")

os.system("systemctl start ePaperRuneaudio")

os.system("systemctl enable ePaperRuneaudio")
