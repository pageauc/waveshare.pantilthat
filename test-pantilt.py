#!/usr/bin/python
from __future__ import print_function
print('Loading ...')
import time
import os
import sys
import RPi.GPIO as GPIO

PROG_VER = '0.9'
PROG_NAME = os.path.basename(__file__)

# Image Settings
IMAGE_PREFIX = 'image-'
IMAGE_DIR = './images'

# Pi Camera Settings
CAMERA_RESOLUTION = (1280, 720)
CAMERA_HFLIP = True
CAMERA_VFLIP = True
CAMERA_WARMUP_SEC = 2
CAMERA_STOPS = [(90, 20),
                (54, 20),
                (18, 20),
                (-18, 20),
                (-54, 20),
                (-90, 20)]

# Servo Settings
SERVO_SLEEP_SEC = 0.1  # Allow time for servo to move
SERVO_SPEED = 2  # degree increment for speed of pan/tilt smooth moves

try:
    import picamera
except ImportError:
    print('ERROR: Could Not import picamera library')
    print('import per commands below\n')
    print('sudo apt-get install python-picamera')
    print('sudo apt-get install python3-picamera')
    sys.exit(1)

try:
    # Try to import from /usr/local/lib/python2.7/dist-packages or python3.7/dist-packages
    from waveshare.pantilthat import PanTilt
except ImportError:
    # import from a local pantilthat.py in same folder as this script.
    from pantilthat import PanTilt

if not os.path.isdir(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Setup pantilt
cam = PanTilt()  # Initialize pantilt servo library
cam.flip_servo = False  # Optionally flips pan and tilt in case servo plugin is different
cam.debug = False
cam.setPWMFreq(50)  # Optional pwm frequency setting
cam.setServoPulse(1, 500)  # Optional pwm servo pulse setting
cam.pan(0)  # center pan
cam.tilt(20) # center tilt slightly higher

#----------------------------------------
def center(pan=0, tilt=0):
    cam.pan(pan)
    time.sleep(SERVO_SLEEP_SEC)
    cam.tilt(tilt)
    time.sleep(SERVO_SLEEP_SEC)

print('-------------------------------------------------')
print('%s ver %s  written by Claude Pageau' % (PROG_NAME, PROG_VER))
print('-------------------------------------------------')
print("This is a WaveShare pantilt assembly Demo using a picamera module.")

try:
  with picamera.PiCamera() as camera:
      camera.resolution = CAMERA_RESOLUTION
      camera.hflip = CAMERA_HFLIP
      camera.vflip = CAMERA_VLIP
      time.sleep(CAMERA_WARMUP_SEC) # Allow time for camera to warm up
      image_seq = 1  # image numbering for a full cam stop sequence
      while True:
        print('center cam at pan=0 tilt=20')
        center(0, 20)
        print("Pan Max Left cam.pan(-90)")
        cam.pan(-90)
        time.sleep(2)
        print("Pan Max Right cam.pan(90)")
        cam.pan(90)
        time.sleep(2)

        img_num = 0  # image number within a cam stop sequence
        print('Take Images at Cam Stops')
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
            camera.capture(filename)
            print('At cam stop(%i, %i) Saved %s' %
                  (pan_stop, tilt_stop, filename))
        image_seq += 1

        print('Smooth Pan Right speed = %i' % SERVO_SPEED)
        for i in range(-90, 90, SERVO_SPEED):
            cam.pan(i)
            time.sleep(SERVO_SLEEP_SEC)

        print('Smooth Pan Left speed = %i' % SERVO_SPEED)
        for i in range(90, -90, -SERVO_SPEED):
            cam.pan(i)
            time.sleep(SERVO_SLEEP_SEC)

        center(0, 20)
        print("Tilt Max Down cam.tilt(-90)")
        cam.tilt(-90)
        time.sleep(2)
        print("Tilt Max Up cam.tilt(90)")
        cam.tilt(90)
        time.sleep(2)

        print('Smooth Pan Down speed = %i' % SERVO_SPEED)
        for i in range(90, -90, -SERVO_SPEED):
            cam.tilt(i)
            time.sleep(SERVO_SLEEP_SEC)
        print('Smooth Pan Up speed = %i' % SERVO_SPEED)
        for i in range(-90, 90, SERVO_SPEED):
            cam.tilt(i)
            time.sleep(SERVO_SLEEP_SEC)
        center(0, 20)

        print('Press ctrl-c to exit demo')
        time.sleep(5)

except KeyboardInterrupt:
  center(0, 20)
  print('pantilthat.py version is %s' % cam.__version__())
  cam.help()
  cam.stop()
  print('\n%s ver %s User Exited with Keyboard ctrl-c' % (PROG_NAME, PROG_VER))
  sys.exit()
