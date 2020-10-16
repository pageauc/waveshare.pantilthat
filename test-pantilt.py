#!/usr/bin/python
from __future__ import print_function
print('Loading ...')
import time
import os
import sys
import RPi.GPIO as GPIO

PROG_VER = '0.96'
PROG_NAME = os.path.basename(__file__)

PANTILT_IS_PIMORONI = False  # Set to True to Test with Pimoroni pantilthat

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
        print('ERROR: Could Not import picamera library')
        print('import per commands below\n')
        print('sudo apt-get install python-picamera')
        print('sudo apt-get install python3-picamera')
        sys.exit(1)

if PANTILT_IS_PIMORONI:
    try:
        import pantilthat
    except ImportError:
        print(Import Error. Install Pimoroni pantilthat python library per')
        print('   sudo apt install python-pantilthat')
        print('   sudo apt install python3-pantilthat') 
        sys.exit()
else:        
    try:
        # Try to import from /usr/local/lib/python2.7/dist-packages or python3.7/dist-packages
        from waveshare.pantilthat import PanTilt
    except ImportError:
        # import from a local pantilthat.py in same folder as this script.
        print('Import error.  Install Waveshare drivers via curl script Reboot and retry test')
        print('curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/install-driver.sh | bash')
        sys.exit()

# Setup pantilt
cam = PanTilt()  # Initialize pantilt servo library
cam.flip_servo = False  # Optionally flips pan and tilt in case servo plugin is different
cam.debug = False
# cam.setPWMFreq(50)  # Optional pwm frequency setting
# cam.setServoPulse(1, 500)  # Optional pwm servo pulse setting
cam.pan(SERVO_PAN_CENTER)   # center pan
cam.tilt(SERVO_TILT_CENTER) # center tilt pointing slightly higher

#----------------------------------------
def center(pan=SERVO_PAN_CENTER, tilt=SERVO_TILT_CENTER):
    cam.pan(pan)
    time.sleep(SERVO_SLEEP_SEC)
    cam.tilt(tilt)
    time.sleep(SERVO_SLEEP_SEC)

#----------------------------------------
def run_demo():
    image_seq = 1  # image numbering for a full cam stop sequence
    print('----- Begin Demo -----')
    while True:
        print('center cam at pan=0 tilt=20')
        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print("Pan Max Left cam.pan(%i)" % SERVO_PAN_MIN)
        cam.pan(SERVO_PAN_MIN)
        time.sleep(2)
        print("Pan Max Right cam.pan(%i)" % SERVO_PAN_MAX)
        cam.pan(SERVO_PAN_MAX)
        time.sleep(2)

        img_num = 0  # image number within a cam stop sequence
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
            cam.tilt(tilt_stop)
            time.sleep(SERVO_SLEEP_SEC)
            cam.pan(pan_stop)
            time.sleep(0.8)  # wait a while to avoid image blur
            if CAMERA_ON:
                camera.capture(filename)
                print('At cam stop(%i, %i) Saved %s' %
                      (pan_stop, tilt_stop, filename))
            else:
                print('Move to cam stop(%i, %i)' % (pan_stop, tilt_stop))
        image_seq += 1

        print('Smooth Pan Right speed = %i' % SERVO_SPEED)
        for pan_pos in range(SERVO_PAN_MIN, SERVO_PAN_MAX, SERVO_SPEED):
            cam.pan(pan_pos)
            time.sleep(SERVO_SLEEP_SEC)

        print('Smooth Pan Left speed = %i' % SERVO_SPEED)
        for pan_pos in range(SERVO_PAN_MAX, SERVO_PAN_MIN, -SERVO_SPEED):
            cam.pan(pan_pos)
            time.sleep(SERVO_SLEEP_SEC)

        center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
        print("Tilt Max Down cam.tilt(%i)" % SERVO_TILT_MAX)
        cam.tilt(SERVO_TILT_MAX)
        time.sleep(2)
        print("Tilt Max Up cam.tilt(%i)" % SERVO_TILT_MIN)
        cam.tilt(SERVO_TILT_MIN)
        time.sleep(2)

        print('Smooth Pan Down speed = %i' % SERVO_SPEED)
        for tilt_pos in range(SERVO_TILT_MIN, SERVO_TILT_MAX, SERVO_SPEED):
            cam.tilt(tilt_pos)
            time.sleep(SERVO_SLEEP_SEC)
        print('Smooth Pan Up speed = %i' % SERVO_SPEED)
        for tilt_pos in range(SERVO_TILT_MAX, SERVO_TILT_MIN, -SERVO_SPEED):
            cam.tilt(tilt_pos)
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
    print('----- End Demo -----')
    center(SERVO_PAN_CENTER, SERVO_TILT_CENTER)
    print('\n%s ver %s User Exited with Keyboard ctrl-c\n' % (PROG_NAME, PROG_VER))
    cam.help()
    cam.stop()
    sys.exit()
