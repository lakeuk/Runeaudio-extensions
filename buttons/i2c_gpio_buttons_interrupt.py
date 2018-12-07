# Store in - /var/www/command
# Script name - gpioRuneaudioi2c.py

#!/usr/bin/env python2

import time
#from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import smbus2 
import os
import subprocess

#variables
#global mpcvol,resetvol,bytempcvol,cmd

# i2c address of each PCF8574 
IOSET1=0x20 
IOSET2=0x21
IOSET3=0x22

# open the bus (0 -- original Pi, 1 -- Rev 2 Pi) 
b=smbus2.SMBus(1) 

# make certain the pins are set high so they can be used as inputs 
b.write_byte(IOSET1, 0xff) 
b.write_byte(IOSET2, 0xff) 
b.write_byte(IOSET3, 0xff)

# Interrupt input pin
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

############# SUB buttonpress #############

def buttonpress(channel):
  pins1 = b.read_byte(IOSET1) 
  pins2 = b.read_byte(IOSET2) 
  pins3 = b.read_byte(IOSET3)   
  if pins1 == 0xfe:
    print "Reboot"
    os.system("shutdown -r now")    
  if pins1 == 0xfd:
    print "Shutdown"
    os.system("shutdown -h now")     
  if pins1 == 0xfb:
    os.system("mpc volume +1")  
    print "Volume Up Pressed+"
    time.sleep(0.5)    
  if pins1 == 0xf7:
    print "Volume Down Pressed"
    os.system("mpc volume -1")
    time.sleep(0.5)    
  if pins1 == 0xef:
    print "Next Station or Track Pressed"
    os.system("mpc next")  
    time.sleep(0.3)
  if pins1 == 0xdf:
    print "Previous Station or Track Pressed"
    os.system("mpc prev") 
    time.sleep(0.3)
  if pins1 == 0xbf:
    print "Play Pause Toggled"
    os.system("mpc toggle") 
    time.sleep(0.2)
  if pins1 == 0x7f:
    print "Stop"
    os.system("mpc stop")

  if pins2 == 0xfe:
    print "Station Preset 10 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 10") 
    time.sleep(0.5)
  if pins2 == 0xfd:
    print "Station Preset 9 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 9") 
    time.sleep(0.5)
  if pins2 == 0xfb:
    print "Station Preset 8 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 8") 
    time.sleep(0.5)
  if pins2 == 0xf7:
    print "Station Preset 6 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 6") 
    time.sleep(0.5)
  if pins2 == 0xef:
    print "Station Preset 4 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 4") 
    time.sleep(0.5)
  if pins2 == 0xdf:
    print "Station Preset 3 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 3") 
    time.sleep(0.5)
  if pins2 == 0xbf:
    print "Station Preset 2 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 2") 
    time.sleep(0.5)
  if pins2 == 0x7f:
    print "Station Preset 1 Pressed"
    os.system("mpc clear")  
    os.system("mpc load 'Radio Preset'")
    os.system("mpc play 1") 
    time.sleep(0.5)

#  if pins3 == 0xfe:
#    #os.system("mpc volume 0")  
#    #print "Volume Muted" 
#    time.sleep(0.5)
#  if pins3 == 0xfd:
#    #os.system("mpc volume 0")  
#    #print "Volume Muted"  
#    time.sleep(0.5)
#  if pins3 == 0xfb: #RotaryButton
#    os.system("mpc volume 90")  
#    print "Volume 90%"    
#    time.sleep(0.5)
#  if pins3 == 0xf7:
#    #os.system("mpc volume 0")  
#    #print "Volume Muted" 
#    time.sleep(0.5)
#  if pins3 == 0xef:
#    #os.system("mpc volume 0") 
#    os.system("mpc volume -1")  
#    time.sleep(0.01)    
#  if pins3 == 0xdf:
#    #os.system("mpc volume 0")  
#    os.system("mpc volume +1") 
#    time.sleep(0.01)    
#  if pins3 == 0xbf: #RotaryButton
#    cmd = subprocess.Popen("mpc volume",shell=True, stdout=subprocess.PIPE)
#    bytempcvol, err = cmd.communicate()  
#    mpcvol = bytempcvol.decode()
#    mpcvol = int(mpcvol.replace("volume:","").replace(" ","").split('%')[0])
#    if mpcvol > 0:
#      global resetvol
#      resetvol = mpcvol
#      os.system("mpc volume 0")  
#      print "Volume Muted"  
#      time.sleep(0.5)
#    else:
#      resetvol == 95
#      os.system("mpc volume " + str(resetvol))
#      print "Reset to previous: Volume " + str(resetvol) + "%"
#      time.sleep(0.5)      
#  if pins3 == 0x7f:
#    time.sleep(0.5)
   
  #print "%02x" % pins1 
  #print "%02x" % pins2  
  #print "%02x" % pins3
  #time.sleep(0.5)




############# MAIN #############

#GPIO.add_event_detect(26, GPIO.FALLING, callback=buttonpress, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=buttonpress)

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