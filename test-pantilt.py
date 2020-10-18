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
import RPi.GPIO as GPIO

PROG_VER = '0.97'
PROG_NAME = os.path.basename(__file__)
PANTILT_IS_PIMORONI = False  # False= Waveshare or Compatible Pantilthat True= Pimoroni

# Pi Camera Settings
CAMERA_ON = False  # True= Use Picamera  False= Do Not use PiCamera or Not Installed
CAMERA_RESOLUTION = (1280, 720)
CAMERA_HFLIP = True
CAMERA_VFLIP = True
CAMERA_WARMUP_SEC = 2
CAMERA_STOPS = [(90, -10),
                (54, -10),
                (18, -10),
                (-18, -10),
                (-54, -10),
                (-90, -10)]

# Image Settings
IMAGE_PREFIX = 'image-'
IMAGE_DIR = './images'

# Servo Settings
SERVO_SLEEP_SEC = 0.1  # Allow time for servo to move
SERVO_SPEED = 2  # degree increment for speed of pan/tilt smooth moves
SERVO_PAN_CENTER = 0
SERVO_PAN_MIN = -90
SERVO_PAN_MAX = 90
SERVO_TILT_CENTER = -10  # point slightly higher Adjust to your needs
SERVO_TILT_MIN = -90
SERVO_TILT_MAX = 90

if CAMERA_ON:
    try:
        import picamera
    except ImportError:
        print('ERROR: Could Not import picamera python library')
        print('Install python libraries per commands below\n')
        print('sudo apt-get install python-picamera')
        print('sudo apt-get install python3-picamera')
        sys.exit(1)

if PANTILT_IS_PIMORONI:
    try:
        import pantilthat
    except ImportError:
        print('ERROR : Import Pimoroni PanTiltHat Python Library per')
        print('        sudo apt install pantilthat')
        sys.exit()
    try:
        pantilthat.pan(SERVO_PAN_CENTER)
    except IOError:
        print('ERROR: pantilthat hardware problem')
        print('nano edit this script, change variable and retry per')
        print('    nano -l %s' % PROG_NAME)
        print('Change value of variable per below. ctrl-x y to save and exit')
        print('    PANTILT_IS_PIMORONI = False')
        sys.exit()
    pantilt_is = 'Pimoroni'
else:
    try:
        # import pantilthat
        from waveshare.pantilthat import PanTilt
    except ImportError:
        print('ERROR : Install Waveshare PanTiltHat Python Library per')
        print('        curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/install.sh | bash')
        sys.exit()
    try:
        pantilthat = PanTilt()
        pantilthat.pan(SERVO_PAN_CENTER)
    except IOError:
        print('ERROR: pantilthat hardware problem')
        print('nano edit this script, change variable below and retry per')
        print('    nano -l %s' % PROG_NAME)
        print('Change value of variable per below. ctrl-x y to save and exit')
        print('    PANTILT_IS_PIMORONI = True')
        sys.exit()
    pantilt_is = 'Waveshare'

# Setup pantilt
pantilthat.flip_servo = False  # Optionally flips pan and tilt in case servo plugin is different
pantilthat.debug = False
# pantilthat.setPWMFreq(50)  # Optional pwm frequency setting
# pantilthat.setServoPulse(1, 500)  # Optional pwm servo pulse setting
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
    image_seq = 1  # image numbering for a full pantilthat stop sequence
    print('----- Begin %s Demo -----' % pantilt_is)
    while True:
        print('center pantilthat at pan=0 tilt=20')
        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print("Pan Max Left pantilthat.pan(%i)" % SERVO_PAN_MIN)
        pantilthat.pan(SERVO_PAN_MIN)
        time.sleep(2)
        print("Pan Max Right pantilthat.pan(%i)" % SERVO_PAN_MAX)
        pantilthat.pan(SERVO_PAN_MAX)
        time.sleep(2)

        img_num = 0  # image number within a pantilthat stop sequence
        print('CAMERA_ON = %s' % CAMERA_ON)
        if CAMERA_ON:
            print('Take Images at Cam Stops')
        else:
            print('Move to Cam Stops')
        for stop in CAMERA_STOPS:
            pan_stop, tilt_stop = stop
            img_num += 1
            filename = os.path.join(IMAGE_DIR,
                                    IMAGE_PREFIX +
                                    'seq' + str(image_seq) +
                                    '-' + str(img_num) + '.jpg')
            pantilthat.tilt(tilt_stop)
            time.sleep(SERVO_SLEEP_SEC)
            pantilthat.pan(pan_stop)
            time.sleep(0.8)  # wait a while to avoid image blur
            if CAMERA_ON:
                camera.capture(filename)
                print('At pantilthat stop(%i, %i) Saved %s' %
                      (pan_stop, tilt_stop, filename))
            else:
                print('Move to pantilthat stop(%i, %i)' % (pan_stop, tilt_stop))
        image_seq += 1

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

print('-------------------------------------------------')
print('%s ver %s  written by Claude Pageau' % (PROG_NAME, PROG_VER))
print('-------------------------------------------------')
print("This is a WaveShare pantilt assembly Demo.")
try:
    if CAMERA_ON:
        # Create image directory if required
        if not os.path.isdir(IMAGE_DIR):
            print('Create IMAGE_DIR %s' % IMAGE_DIR)
            os.makedirs(IMAGE_DIR)

        print('Initializing PiCamera ....')
        with picamera.PiCamera() as camera:
            camera.resolution = CAMERA_RESOLUTION
            camera.hflip = CAMERA_HFLIP
            camera.vflip = CAMERA_VFLIP
            time.sleep(CAMERA_WARMUP_SEC) # Allow time for camera to warm up
            run_demo()
    else:
        run_demo()

except KeyboardInterrupt:
    print('')
    print('----- End %s Demo -----' % pantilt_is)
    center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
    print('\n%s ver %s User Exited with Keyboard ctrl-c\n' % (PROG_NAME, PROG_VER))
    if not PANTILT_IS_PIMORONI:
        pantilthat.help()
        pantilthat.stop()
    sys.exit()
