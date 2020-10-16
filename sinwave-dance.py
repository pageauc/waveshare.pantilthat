#!/usr/bin/python
'''
sinwave-dance.py is Adapted from the Pimoroni github smooth.py example
Modified by Claude Pageau to add support for Waveshare pantilthat.

'''
import sys
import math
import time
import RPi.GPIO as GPIO

VERBOSE_ON = False  # Default=False True= Display Position data
SPEED = 0.005  # Default 0.005 short Time delay for each loop 
PANTILT_IS_PIMORONI = False  # False= Waveshare or Compatible Pantilthat True= Pimoroni
PAN_HOME = 0  # Center pan to a central position
TILT_HOME = 0  # Center tilt to a central position

if PANTILT_IS_PIMORONI:
    try:
        import pantilthat
    except ImportError:
        print('ERROR : Import Pimoroni PanTiltHat Python Library per')
        print('        sudo apt install pantilthat')
        sys.exit()
    pantilt_is = 'Pimoroni'
else:
    try:
        # import pantilthat
        from waveshare.pantilthat import PanTilt
    except ImportError:
        print('ERROR : Install Waveshare PanTiltHat Python Library per')
        print('        curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/install.sh | bash')
        sys.exit
    pantilthat = PanTilt()
    pantilt_is = 'Waveshare'

def dance():
  while True:
      # Get the time in seconds
      t = time.time()

      # G enerate an angle using a sine wave (-1 to 1) multiplied by 90 (-90 to 90)
      a = math.sin(t * 2) * 90

      # Cast a to int for v0.0.2
      a = int(a)

      pantilthat.pan(a)
      pantilthat.tilt(a)

      # Two decimal places is quite enough!
      if VERBOSE_ON:
          print(round(a, 2))

      # Sleep for a bit so we're not hammering the HAT with updates
      time.sleep(SPEED)

try:
    print('Start %s PanTiltHat SinWave Dance Ctrl-c to Exit' %
           pantilt_is)
    dance()
except KeyboardInterrupt:
    pantilthat.pan(PAN_HOME)
    pantilthat.tilt(TILT_HOME)
    time.sleep(0.1)  # Short delay to move servos
    pantilthat.stop() # Turn off PWM to servos
    print('\nUser Pressed ctrl-c')
    print('Position of PanTilt is (%i, %i)' % (PAN_HOME, TILT_HOME))
    print('End %s PanTiltHat SinWave Dance' % pantilt_is)
    print('Bye ...')
