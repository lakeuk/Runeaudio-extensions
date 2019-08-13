# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCF8574
# This code is designed to work with the PCF8574_LBAR_I2CL I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus2
import time
import os
import subprocess

ADDR=0x22
VALUE = 0xFF #All pins configured as inputs

LastAPIN = 0
APIN = 0
BPIN = 0
volumecnt = 0
clkLastState = 1

LastAPIN2 = 0
APIN2 = 0
BPIN2 = 0
volumecnt2 = 0
clkLastState2 = 1

#Get current volume
cmd = subprocess.Popen("mpc volume",shell=True, stdout=subprocess.PIPE)
bytempcvol, err = cmd.communicate()  
mpcvol = bytempcvol.decode()
mpcvol = int(mpcvol.replace("volume:","").replace(" ","").split('%')[0])
volumecnt = mpcvol

# Get I2C bus
bus = smbus2.SMBus(1)

# PCF8574 address, 0x22(32) #0xFF(255)	All pins configured as inputs
bus.write_byte(ADDR, VALUE)
time.sleep(0.5)
        
while True:
  # PCF8574 address, 0x22(32) # Read data back, 1 byte
  data = bus.read_byte(ADDR)

  # Convert the data
  data = (data & 0xFF)

  clkState = data & (2 ** 4) #Pin4-CLK
  dtState = data & (2 ** 5) #Pin5-DT
  button1 = data & (2 ** 6) #Pin6-button
  
  clkState2 = data & (2 ** 0) #Pin0-CLK
  dtState2 = data & (2 ** 1) #Pin1-DT  
  button2 = data & (2 ** 2) #Pin2-button

#################### Rotary 1 - Rotary 1 ####################

  if clkState == 16: APIN = 1 
  else: APIN = 0  
  if dtState == 32: BPIN = 1
  else: BPIN = 0  
  
  #if ([clkState,dtState] == [16,32]):
  #  print("HIGH HIGH" + " " + str(clkState) + " " + str(dtState))
  #elif ([clkState,dtState] == [0,32]):
  #  print("    LOW HIGH" + " " + str(clkState) + " " + str(dtState))
  #elif ([clkState,dtState] == [0,0]):
  #  print("        LOW LOW" + " " + str(clkState) + " " + str(dtState))
  #elif ([clkState,dtState] == [16,0]):
  #  print("            HIGH LOW" + " " + str(clkState) + " " + str(dtState))
 
  if APIN != LastAPIN:
    if BPIN != APIN:
      volumecnt += 1
    else:
      volumecnt -= 1
      
    if volumecnt < 0: volumecnt = 0  
    if volumecnt > 100: volumecnt = 100
    #print(volumecnt)
    os.system("mpc volume " + str(volumecnt))
  LastAPIN = APIN
  #time.sleep(0.05)    

#################### Rotary 2 - Rotary 2 ####################

  if clkState2 == 1: APIN2 = 1 
  else: APIN2 = 0  
  if dtState2 == 2: BPIN2 = 1
  else: BPIN2 = 0  
  
  if APIN2 != LastAPIN2:
    if BPIN2 != APIN2:
      volumecnt += 1
    else:
      volumecnt -= 1
      
    if volumecnt < 0: volumecnt = 0  
    if volumecnt > 100: volumecnt = 100
    #print(volumecnt)
    os.system("mpc volume " + str(volumecnt))
  LastAPIN2 = APIN2
  #time.sleep(0.05)    

#################### Rotary 1 - Button ####################

  if button1 == 0: #RotaryButton
    cmd = subprocess.Popen("mpc volume",shell=True, stdout=subprocess.PIPE)
    bytempcvol, err = cmd.communicate()  
    mpcvol = bytempcvol.decode()
    mpcvol = int(mpcvol.replace("volume:","").replace(" ","").split('%')[0])
    if mpcvol > 0:
      global resetvol
      resetvol = mpcvol
      os.system("mpc volume 0")  
      print("Volume Muted")  
      time.sleep(0.5)
    else:
      resetvol == 95
      os.system("mpc volume " + str(resetvol))
      print("Reset to previous: Volume " + str(resetvol) + "%")
      time.sleep(0.5)

#################### Rotary 2 - Button ####################
      
  if button2 == 0: #RotaryButton
    cmd = subprocess.Popen("mpc volume",shell=True, stdout=subprocess.PIPE)
    bytempcvol2, err = cmd.communicate()  
    mpcvol2 = bytempcvol2.decode()
    mpcvol2 = int(mpcvol2.replace("volume:","").replace(" ","").split('%')[0])
    if mpcvol2 > 0:
      global resetvol2
      resetvol2 = mpcvol2
      os.system("mpc volume 0")  
      print("Volume Muted") 
      time.sleep(0.5)
    else:
      resetvol2 == 95
      os.system("mpc volume " + str(resetvol2))
      print("Reset to previous: Volume " + str(resetvol2) + "%")
      time.sleep(0.5)      