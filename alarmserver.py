#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import os
try:
  from urlparse import urlparse
except ImportError:
  from urllib.parse import urlparse

# Change these variables to your script locations
# As for what these scripts should do, I recommend calling something like aplay or mplay to play the desired sound. 
# I also use SSH in these scripts to play aounds on several raspis throughout the house. 
# I use cheap battery-backed bluetooth speakers connected to the headphone jack of a cheap USB sound interface on the raspi
# USB sound devices are prefered due to the fact that the headphone output of the raspi is quite noisy

SCRIPT_ARM_AWAY = '/home/pi/scripts/armedaway.sh'
SCRIPT_ARM_HOME = '/home/pi/scripts/armedawayquiet.sh'
SCRIPT_DISARM_AWAY = '/home/pi/scripts/disarmed.sh'
SCRIPT_DISARM_HOME = '/home/pi/scripts/disarmedquiet.sh'
SCRIPT_ALARM_TRIGGER = '/home/pi/scripts/alarm.sh'
SAVESTATE_FILE = '/home/pi/alarmstate.txt'

# Initial state (used only if no saved state exists, don't change this)
current_state = 'disarmed';

# Main request handler, see URLs below for the endpoints to use in your home automation system
class alarmRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    request_path = urlparse(self.path).path
    print('Request path: ' + request_path)
    responsecode = 200
    responsemessage = 'Succcess';

    # Configure your home automation system to send http get request to http://yourserver/arm_away when you leave the house
    if (request_path == '/arm_away'):
      alarm_arm_away()
    # Configure your home automation system to send http get request to http://yourserver/disarm_away when you return home
    elif (request_path == '/disarm_away'):
      alarm_disarm()
    # Configure your home automation system to send http get request to http://yourserver/arm_home when you arm the system while staying at home
    elif (request_path == '/arm_home'):
      alarm_arm_home()
    # Configure your home automation system to send http get request to http://yourserver/disarm_home when you disarm the system while staying at home
    elif (request_path == '/disarm_home'):
      alarm_home()
    # Configure your home automation system to send http get request to http://yourserver/trigger_away if your motion sensors detect movement
    elif (request_path == '/trigger_away'):
      if (current_state == 'armed_away' or current_state == 'armed_home'):
        alarm_trigger()
    # Configure your home automation system to send http get request to http://yourserver/trigger_home if your glass or door sensors are triggered
    elif (request_path == '/trigger_home'):
      if (current_state == 'armed_home'):
        alarm_trigger()
    else:
      responsecode = 305
      responsemessage = 'Unknown Operation';

    # Send response
    self.send_response(responsecode)
    self.send_header('Content-type','text/html')
    self.end_headers()
    self.wfile.write(bytes(responsemessage, "utf8"))
    return

# Persists current alarm state (armed, disarmed, etc)
def savestate(state):
  current_state = state;
  file = open(SAVESTATE_FILE, 'w')
  file.write(state)
  file.close()
  return

# Load state from file, performed on startup
def loadstate():
  state='disarmed'
  try:
    file = open(SAVESTATE_FILE, 'r')
    state = file.read()
  except OSError:
    pass
  return state

# Call script for arming as you leave the house. 
# On my system this plays a loud arming announcement throughout the house.
def alarm_arm_away():
  os.system(SCRIPT_ARM_AWAY)  
  savestate('armed_away')
  return

# Call script for drming while at home. 
# On my system this plays a more quiet arming sound throughout the house.
def alarm_arm_home():
  os.system(SCRIPT_ARM_HOME)
  savestate('armed_home')
  return

# Call script for disarming as come back home. 
# On my system this plays a loud disarming announcement throughout the house.
def alarm_disarm_away():
  os.system(SCRIPT_DISARM_AWAY)
  savestate('disarmed')
  return

# Call script for disarming while at home. 
# On my system this plays a more quiet disarming sound throughout the house.
def alarm_disarm_home():
  os.system(SCRIPT_DISARM_HOME)
  savestate('disarmed')
  return

# Call script for actions to be performed when an alarm is triggered. 
# On my system this plays a 3 minute long alarm klaxon sound throughout the house.
def alarm_trigger():
  os.system(SCRIPT_ALARM_TRIGGER)
  savestate('alarm')
  return

def run():
  current_state = loadstate()
  if (current_state == ''):
    savestate('disarmed')
  print('loading state: ' + current_state)

  print('starting server...')
  server_address = ('0.0.0.0', 8081)
  httpd = HTTPServer(server_address, alarmRequestHandler)
  print('running server...')
  httpd.serve_forever()

run()
