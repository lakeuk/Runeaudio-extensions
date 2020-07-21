# Store in - /home/myapp/buttons
# Script name - i2c_gpio_buttons_interrupt.py

#!/usr/bin/env python3

import time
#from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import smbus2 
import os

# open the bus (0 -- original Pi, 1 -- Rev 2 Pi)
b=smbus2.SMBus(1)

# i2c address of each PCF8574 
IOSET1=0x20 
IOSET2=0x21
IOSET3=0x22

# make certain the pins are set high so they can be used as inputs 
b.write_byte(IOSET1, 0xff) 
b.write_byte(IOSET2, 0xff) 
b.write_byte(IOSET3, 0xff)

def execCmd(action, cmdlist):
  print(action)
  for cmd in cmdlist:
    os.system(cmd)
  time.sleep(0.2)

def buttonpress(channel):
  pins1 = b.read_byte(IOSET1) 
  pins2 = b.read_byte(IOSET2) 
  pins3 = b.read_byte(IOSET3)

  execCmd('Reboot', ["shutdown -r now"]) if pins1 == 0xfe else False
  execCmd('Shutdown', ["shutdown -h now"]) if pins1 == 0xfd else False
  execCmd('Volume Up Pressed+', ["mpc volume +1"]) if pins1 == 0xfb else False
  execCmd('Volume Down Pressed-', ["mpc volume -1"]) if pins1 == 0xf7 else False
  execCmd('Next Station or Track Pressed', ["mpc next"]) if pins1 == 0xef else False
  execCmd('Previous Station or Track Pressed', ["mpc prev"]) if pins1 == 0xdf else False
  execCmd('Play Pause Toggled', ["mpc toggle"]) if pins1 == 0xbf else False
  execCmd('Stop', ["mpc stop"]) if pins1 == 0x7f else False

  execCmd('Station Preset 10 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 10"]) if pins2 == 0xfe else False
  execCmd('Station Preset 9 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 9"]) if pins2 == 0xfd else False
  execCmd('Station Preset 8 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 8"]) if pins2 == 0xfb else False
  execCmd('Station Preset 6 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 6"]) if pins2 == 0xf7 else False
  execCmd('Station Preset 4 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 4"]) if pins2 == 0xef else False
  execCmd('Station Preset 3 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 3"]) if pins2 == 0xdf else False
  execCmd('Station Preset 2 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 2"]) if pins2 == 0xbf else False
  execCmd('Station Preset 1 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 1"]) if pins2 == 0x7f else False

  #execCmd('Station Preset 10 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 10"]) if pins3 == 0xfe else False
  #execCmd('Station Preset 9 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 9"]) if pins3 == 0xfd else False
  #execCmd('Station Preset 8 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 8"]) if pins3 == 0xfb else False
  #execCmd('Station Preset 6 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 6"]) if pins3 == 0xf7 else False
  #execCmd('Station Preset 4 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 4"]) if pins3 == 0xef else False
  #execCmd('Station Preset 3 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 3"]) if pins3 == 0xdf else False
  #execCmd('Station Preset 2 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 2"]) if pins3 == 0xbf else False
  #execCmd('Station Preset 1 Pressed', ["mpc clear", "mpc load 'Radio Preset'", "mpc play 1"]) if pins3 == 0x7f else False

  #print("%02x" % pins1) 
  #print("%02x" % pins2)  
  #print("%02x" % pins3)

############# MAIN #############

# Set state for interrupt input pin
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Detect interrupt activation
GPIO.add_event_detect(26, GPIO.FALLING, callback=buttonpress)
#GPIO.add_event_detect(26, GPIO.FALLING, callback=buttonpress, bouncetime=300)

while True:
  time.sleep(10)

###############################################################

#IOSET1 - 0x20
#0 fe
#1 fd
#2 fb Volume+
#3 f7 Volume-
#4 ef Next
#5 df Prev
#6 bf Toggle
#7 7f Stop
#IOSET2 - 0x21
#0 fe Preset8
#1 fd Preset7
#2 fb Preset6
#3 f7 Preset5
#4 ef Preset4
#5 df Preset3
#6 bf Preset2
#7 7f Preset1
#IOSET3 - 0x22
#0 fe rotary2 CLK 
#1 fd rotary2 DT 
#2 fb rotary2 pushbutton-switch 
#3 f7 rotary2 +
#4 ef rotary1 CLK
#5 df rotary1 DT
#6 bf rotary1 pushbutton-switch -VolumeMute
#7 7f rotary1 +