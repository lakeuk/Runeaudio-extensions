#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import os
import sys
import time
import subprocess
import re

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

#epaper imports
import logging
import epd2in9
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#logging.basicConfig(level=logging.DEBUG)

pathbmp = '/home/myapp/epaper/bmp/'
#arrbmp = ['BBC Radio 1','BBC Radio 2','BBC Radio 4 FM','BBC Radio 4 Extra','BBC Radio 5 Live UK','BBC 6 Music','LBC UK','Forth 1','Rock FM','Virgin Radio UK','Lakeland Radio 100.1, 100.8 & 101.4 FM','The Bay 96.9 FM','BBC Radio Cumbria','BBC Radio Lancashire','BBC Radio Manchester','Smooth Lake District','Heart North Lancs & Cumbria','Bay Trust Radio','CandoFM','Key 103']
arrbmp = os.listdir(pathbmp)
for i, item in enumerate(arrbmp):
  arrbmp[i]=item[:-4]

## epaper functions
def epaperReset():
  epd = epd2in9.EPD()
  epd.init(epd.lut_full_update)
  epd.Clear(0xFF)  
  # For simplicity, the arguments are explicit numerical coordinates
  #image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
  #epd.display(epd.getbuffer(image)) 

def drawbmpFull(imagename):
  epd = epd2in9.EPD()
  epd.init(epd.lut_full_update) 
  epd.Clear(0xFF)  
  image = Image.open(pathbmp + imagename +'.bmp')
  image = image.transpose(Image.ROTATE_90)  
  epd.display(epd.getbuffer(image))  
  epd.sleep()

def drawbmpPart(imagename):
  epd = epd2in9.EPD()
  epd.init(epd.lut_partial_update) 
  epd.Clear(0xFF)  
  image = Image.open(pathbmp + imagename + '.bmp')
  image = image.transpose(Image.ROTATE_90)  
  epd.display(epd.getbuffer(image))   
  epd.sleep()
## epaper functions end

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
def mpdConnect(client, con_id):
  """
  Simple wrapper to connect MPD.
  """
  try:
    client.connect(**con_id)
  except SocketError:
    return False
  return True

def mpdAuth(client, secret):
  """
  Authenticate
  """
  try:
    client.password(secret)
  except CommandError:
    return False
  return True
##

def main():
## MPD object instance
  client = MPDClient()
  if mpdConnect(client, CON_ID):
    print('Got connected!')
  else:
    print('fail to connect MPD server.')
    sys.exit(1)

# Auth if password is set non False
  if PASSWORD:
    if mpdAuth(client, PASSWORD):
      print('Pass auth!')
    else:
      print('Error trying to pass auth.')
      client.disconnect()
      sys.exit(2)

  laststation = 0
  laststate = 0

  while(1):

    client.send_idle()
    state = client.fetch_idle()

    if (state[0] == 'mixer'):
      print('Volume = ' + client.status()['volume'])
      time.sleep(0.2)

    if (state[0] == 'player'):
      time.sleep(0.2)        

    try:
      #station = client.currentsong()['name']
      station_url = subprocess.check_output("mpc -f %file% current", stderr=subprocess.STDOUT, shell=True) # http://mystreamurl/;?station_name=MY_STATION_NAME
      station_url = station_url.decode('ISO-8859-1') # Resolves::TypeError: cannot use a string pattern on a bytes-like object
      station = re.findall(r'\?station_name=(.*)', station_url)  # ['MY_STATION_NAME']
      if len(station) > 0:
        station = station[0].replace('_', ' ')  # MY STATION NAME
      else:
        station = ''
      #print(station)
    except KeyError:
      station = ''

    try:
      state = client.status()['state']
    except KeyError:
      state = ''

    try:
      title = client.currentsong()['title']
    except KeyError:
      title = ''

    try:
      artist = client.currentsong()['artist']
    except KeyError:
      artist = ''

    if(station != ''):    # webradio
      #print('Station = ' + station)
      if laststation != station:
        #print(station)
        if station in arrbmp:
          print(station + ' - logo available')
          #epaperReset()
          #drawbmpPart(station)  
          drawbmpFull(station)
        else:
          print(station + ' - no logo available')                  
          #epaperReset()                    
          #drawbmpPart('default')
          drawbmpFull('default')                    
      #print('Title = ' + title)
        laststation = station
      elif(laststate == 'stop' and state == 'play'):
        if station in arrbmp:
          print(station + ' - logo available - stop-play')
          #epaperReset()
          #drawbmpPart(station)   
          drawbmpFull(station)
        else:
          print(station + ' - no logo available - stop-play')                  
          #epaperReset()
          #drawbmpPart('default')
          drawbmpFull('default')                    
      laststate = 'play'                  
    #else:                 # file
      #print('Title = ' + title)
      #print('Artist = ' + artist)

    if(state == 'stop'):
      time.sleep(0.5) # support button radiopreset change (as playlist is clear and reloaded, triggering a STOP)
      try:
        statenow = client.status()['state']
      except KeyError:
        state = ''
      print('State: ' + state + ' - statenow: ' + statenow)
      if(statenow == 'stop'): # confirms proper STOP and not a button playlist change
        print('statenow stop')
        drawbmpFull('blank')
        #drawbmpPart('blank')
        laststate = 'stop'

    #if (state[0] == 'playlist'):
    #  print('the current playlist has been modified')

    #if (state[0] == 'database'): 
    #  print('the song database has been modified after update')

    #if (state[0] == 'update'): 
    #  print('a database update has started or finished. If the database was modified during the update, the database event is also emitted.')

    #if (state[0] == 'stored_playlist'): 
    #  print('a stored playlist has been modified, renamed, created or deleted')

    #if (state[0] == 'output'): 
    #  print('an audio output has been enabled or disabled')

    #if (state[0] == 'options'): 
    #  print('options like repeat, random, crossfade, replay gain')

    #if (state[0] == 'sticker'): 
    #  print('the sticker database has been modified.')

  ## disconnect
  client.disconnect()
  print("end of script - client disconnected")
  sys.exit(0)

def test():
  #try:
    epaperReset()
    print("step 1")
    epaperReset()
    print("step 2")    
    epaperReset()
    print("step 3")    
    drawbmpPart('BBC Radio 1')
    print("step 4")    
    time.sleep(10)  
    epaperReset()
    print("step 5")    
    drawbmpPart('BBC Radio 2')
    print("step 6")    
    time.sleep(2)  

  #except IOError as e:
  #  logging.info(e)

  #except KeyboardInterrupt:    
  #  logging.info("ctrl + c:")
  #  epd2in9.epdconfig.module_exit()
  #  exit()

# Script starts here
if __name__ == "__main__":
  main()
  #test()