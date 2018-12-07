#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import os
import sys
import time

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

#epaper imports
import epd2in9
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

pathbmp = '/home/myapp/epaper/bmp/'
#arrbmp = ['BBC Radio 1','BBC Radio 2','BBC Radio 4 FM','BBC Radio 4 Extra','BBC Radio 5 Live UK','BBC 6 Music','LBC UK','Forth 1','Rock FM','Virgin Radio UK','Lakeland Radio 100.1, 100.8 & 101.4 FM','The Bay 96.9 FM','BBC Radio Cumbria','BBC Radio Lancashire','BBC Radio Manchester','Smooth Lake District','Heart North Lancs & Cumbria','Bay Trust Radio','CandoFM','Key 103']
arrbmp = os.listdir(pathbmp)
for i, item in enumerate(arrbmp):
  arrbmp[i]=item[:-4]

## epaper functions
def epaperReset():
  epd = epd2in9.EPD()
  epd.init(epd.lut_full_update)
  # For simplicity, the arguments are explicit numerical coordinates
  image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
  epd.set_frame_memory(image, 0, 0)
  epd.display_frame()
  epd.set_frame_memory(image, 0, 0)
  epd.display_frame()

def drawbmpFull(imagename):
  epd = epd2in9.EPD()
  epd.init(epd.lut_full_update)  
  image = Image.open(pathbmp + imagename +'.bmp')
  image = image.transpose(Image.ROTATE_90)  
  epd.clear_frame_memory(0xFF)
  epd.set_frame_memory(image, 0, 0)
  epd.display_frame() 

def drawbmpPart(imagename):
  epd = epd2in9.EPD()
  epd.init(epd.lut_partial_update) 
  image = Image.open(pathbmp + imagename + '.bmp')
  image = image.transpose(Image.ROTATE_90)  
  epd.clear_frame_memory(0xFF)  
  epd.set_frame_memory(image, 0, 0)
  epd.display_frame()
  epd.set_frame_memory(image, 0, 0)
  epd.display_frame()
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

        if (state[0] == 'player'):
            time.sleep(0.2)        

            try:
                station = client.currentsong()['name']
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
                  print(station)
                  if station in arrbmp:
                    print('logo available')
                    #drawbmpPart('blank')
		    epaperReset()                    
                    drawbmpPart(station)  
                    #drawbmpFull(station)                    
                  else:
                    print('no logo available')                  
                    #drawbmpPart('blank')
 		    epaperReset()                    
                    drawbmpPart('default')
		    #drawbmpFull('default')                    
                    #drawbmpPart('allblack')                    
                #print('Title = ' + title)
                  laststation = station
            	elif(laststate == 'stop' and state == 'play'):
            	  if station in arrbmp:
                    print('logo available - stop-play')
                    #drawbmpPart('blank')
                    epaperReset()
                    drawbmpPart(station)   
		    #drawbmpFull(station)
                  else:
                    print('no logo available - stop-play')                  
                    #drawbmpPart('blank')
                    epaperReset()
                    drawbmpPart('default')
                    #drawbmpFull('default')                    
                    #drawbmpPart('allblack') 
                laststate = 'play'                  
            else:                 # file
                print('Title = ' + title)
                print('Artist = ' + artist)

	    if(state == 'stop'):
	    	print('State ' + state)
                drawbmpFull('allblack')  
                drawbmpPart('blank')                
                #drawbmpPart('default')	
                laststate = 'stop'
                
		
		
		
#        if (state[0] == 'playlist'):
#            print('the current playlist has been modified')

#        if (state[0] == 'database'): 
#           print('the song database has been modified after update')

#        if (state[0] == 'update'): 
#           print('a database update has started or finished. If the database was modified during the update, the database event is also emitted.')

#        if (state[0] == 'stored_playlist'): 
#           print('a stored playlist has been modified, renamed, created or deleted')

#        if (state[0] == 'output'): 
#           print('an audio output has been enabled or disabled')

#        if (state[0] == 'options'): 
#           print('options like repeat, random, crossfade, replay gain')

#        if (state[0] == 'sticker'): 
#           print('the sticker database has been modified.')

    ## disconnect
    client.disconnect()
    sys.exit(0)

# Script starts here
if __name__ == "__main__":
    main()
