import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

lastmpcstation = ""
lastmpcvol = ""

def mpc_station_vol():
  cmd = subprocess.Popen("mpc current",shell=True, stdout=subprocess.PIPE)
  bytempcvol, err = cmd.communicate()  
  mpcstation = bytempcvol.decode()

  cmd = subprocess.Popen("mpc volume",shell=True, stdout=subprocess.PIPE)
  bytempcvol, err = cmd.communicate()  
  mpcvol = bytempcvol.decode()
  mpcvol = int(mpcvol.replace("volume:","").replace(" ","").split('%')[0])
  return mpcstation, mpcvol

RST = None     # on the PiOLED this pin isnt used
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) # 128x32 display with hardware I2C
disp.begin() # Initialize library.
disp.clear() # Clear display.
disp.display()
width = disp.width
height = disp.height 

image = Image.new('1', (width, height)) # Create blank image for drawing. Make sure to create image with mode '1' for 1-bit color.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image.
draw.rectangle((0,0,width,height), outline=0, fill=0) # Draw a black filled box to clear the image.

padding = -2
top = padding
bottom = height-padding
x = 0 # Move left to right keeping track of the current x position for drawing shapes.
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)

while True:
  marktime = round(time.time())
  waittime = 10 #seconds

  while marktime + waittime > round(time.time()):
    mpcstation, mpcvol = mpc_station_vol()
    if mpcvol != lastmpcvol or mpcstation != lastmpcstation:
      marktime = round(time.time())
      #print(marktime)

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), str(mpcstation), font=font, fill=255)
    draw.text((x, top+16), "Volume " + str(mpcvol) + "%", font=font, fill=255)
    disp.image(image) # set display image
  
    if mpcstation != lastmpcstation or mpcvol != lastmpcvol:
      disp.display()

    lastmpcstation = mpcstation
    lastmpcvol = mpcvol
  
  disp.clear()
  disp.display()
