# Store in - /var/www/command
# Script name - *.py

#!/usr/bin/env python2

import sys
import os

parm = sys.argv
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if len(sys.argv) == 3:
  scriptname=parm[0]
  url=parm[1]
  duration=parm[2]
else:
  #for script testing
  url="http://media-the.musicradio.com:80/LBCUK"
  duration=10
  
#default rec directory
output_directory="/home/myapp/recordings/"

#print url
#print duration

#print "streamripper "+ url + " -d " + output_directory + "-l " + str(duration) + " -a %S_%d -o always"

os.system("streamripper "+ url + " -d " + output_directory + " -l " + str(duration) + " -a %S_%d -o always -u listenagain --quiet") 

#Example
#streamripper http://media-the.musicradio.com:80/LBCUK -d /home/myapp/recordings



