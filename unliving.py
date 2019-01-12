#!/usr/bin/python
#Taner Körükmez
#e-mail: tnr.kmz@yandex.com
import RPi.GPIO as GPIO
import sys
import os
import subprocess
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)

GPIO_PIR = 23

print "PIR Module Video Trigger (CTRL-C to exit)"

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0
#Movie path
moviepath = '/home/pi/unliving/media/female.mp4'

try:
  print "Waiting for PIR to settle ..."
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0    
  print "  Ready"
  # Play with Omxplayer start 
  omxprocess = subprocess.Popen(['omxplayer',moviepath,'--orientation=90','--loop'],stdin=subprocess.PIPE)
  time.sleep(2) #Wait stable picture
  omxprocess.stdin.write(b'p')#After start stop and showing first scene
  
  # Loop until users quits with CTRL-C
  while True :
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print "  Motion detected!"
      time.sleep(2)
      omxprocess.stdin.write(b'p')#Paused video is resume now
      
      # Record previous state
      GPIO.output(27,GPIO.HIGH)
      time.sleep(1)
      GPIO.output(27,GPIO.LOW)
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=0
      time.sleep(10) #After start wait 10 sec for video end
      omxprocess.stdin.write(b'<')#Seek video start
    # Wait for 10 milliseconds
    time.sleep(0.01)      
      
except KeyboardInterrupt:
  print "  Quit" 
  # Reset GPIO settings
  GPIO.cleanup()