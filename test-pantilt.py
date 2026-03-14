#!/usr/bin/python
'''
test-pantilt.py written by Claude Pageau
Run pantilthat Demo test routines. Optional PiCamera option avail.
provide various python code examples for others to implement.
This script is compatible with Waveshare, Pimoroni and compatible pantilthat
hardware running under python2 or python3
For more details see https://github.com/pageauc/waveshare.pantilthat
'''

from __future__ import print_function
print('Loading ...')
import time
import os
import sys

PROG_VER = '0.97'
PROG_NAME = os.path.basename(__file__)

print('-------------------------------------------------')
print('%s ver %s  written by Claude Pageau' % (PROG_NAME, PROG_VER))
print("This is a WaveShare/Pimoroni pantilthat assembly Demo.")
print('-------------------------------------------------')


from waveshare.pantilthat import PanTiltController  # This will auto-detect hardware
# Servo Settings
SERVO_SLEEP_SEC = 0.1  # Allow time for servo to move
SERVO_SPEED = 4  # degree increment for speed of pan/tilt smooth moves
SERVO_PAN_CENTER = 0
SERVO_PAN_MIN = -90
SERVO_PAN_MAX = 90
SERVO_TILT_CENTER = -10  # point slightly higher Adjust to your needs
SERVO_TILT_MIN = -90
SERVO_TILT_MAX = 90

# Setup pantilt
pantilthat = PanTiltController()
pantilthat.pan(SERVO_PAN_CENTER)   # center pan
pantilthat.tilt(SERVO_TILT_CENTER) # center tilt pointing slightly higher

#----------------------------------------
def center(pan=SERVO_PAN_CENTER, tilt=SERVO_TILT_CENTER):
    pantilthat.pan(pan)
    time.sleep(SERVO_SLEEP_SEC)
    pantilthat.tilt(tilt)
    time.sleep(SERVO_SLEEP_SEC)

#----------------------------------------
def run_demo():
    print('----- Begin Demo -----')
    while True:
        print('center pantilthat')
        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print("Pan Max Left pantilthat.pan(%i)" % SERVO_PAN_MIN)
        pantilthat.pan(SERVO_PAN_MIN)
        time.sleep(2)
        
        print("Pan Max Right pantilthat.pan(%i)" % SERVO_PAN_MAX)
        pantilthat.pan(SERVO_PAN_MAX)
        time.sleep(2)
        center()

        print('Smooth Pan Right speed = %i' % SERVO_SPEED)
        for pan_pos in range(SERVO_PAN_MIN, SERVO_PAN_MAX, SERVO_SPEED):
            pantilthat.pan(pan_pos)
            time.sleep(SERVO_SLEEP_SEC)

        print('Smooth Pan Left speed = %i' % SERVO_SPEED)
        for pan_pos in range(SERVO_PAN_MAX, SERVO_PAN_MIN, -SERVO_SPEED):
            pantilthat.pan(pan_pos)
            time.sleep(SERVO_SLEEP_SEC)

        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print("Tilt Max Down pantilthat.tilt(%i)" % SERVO_TILT_MAX)
        pantilthat.tilt(SERVO_TILT_MAX)
        time.sleep(2)
        
        print("Tilt Max Up pantilthat.tilt(%i)" % SERVO_TILT_MIN)
        pantilthat.tilt(SERVO_TILT_MIN)
        time.sleep(2)

        print('Smooth Pan Down speed = %i' % SERVO_SPEED)
        for tilt_pos in range(SERVO_TILT_MIN, SERVO_TILT_MAX, SERVO_SPEED):
            pantilthat.tilt(tilt_pos)
            time.sleep(SERVO_SLEEP_SEC)
            
        print('Smooth Pan Up speed = %i' % SERVO_SPEED)
        for tilt_pos in range(SERVO_TILT_MAX, SERVO_TILT_MIN, -SERVO_SPEED):
            pantilthat.tilt(tilt_pos)
            time.sleep(SERVO_SLEEP_SEC)
            
        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print('Press ctrl-c to exit demo')
        time.sleep(5)

try:
   run_demo()
except KeyboardInterrupt:
    print('\n----- End Demo -----')
    print('%s ver %s User Exited with Keyboard ctrl-c\n' % (PROG_NAME, PROG_VER))
    center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
    pantilthat.help()
    pantilthat.stop()
    time.sleep(2)
    sys.exit()
