#!/usr/bin/env python
'''
Simplified SineWave dance demo using unified pantilthat interface
'''
import sys
import math
import time
from waveshare.pantilthat import PanTiltController  # This will auto-detect hardware

SPEED = 0.005  # Time delay for each loop
PAN_HOME = 0   # Center pan position
TILT_HOME = 0  # Center tilt position

def dance():
    print('Start PanTiltHat SineWave Dance (Ctrl-C to exit)')
    
    try:
        while True:
            t = time.time()
            # Generate angle using sine wave (-90 to 90)
            a = int(math.sin(t * 2) * 90)
            
            pantilthat.pan(a)
            pantilthat.tilt(a)
            
            time.sleep(SPEED)
    except KeyboardInterrupt:
        print('\nUser pressed Ctrl-C')
        center_servos()
        sys.exit()

def center_servos():
    """Center the servos and cleanup"""
    print(f'Centering servos at ({PAN_HOME}, {TILT_HOME})')
    pantilthat.pan(PAN_HOME)
    pantilthat.tilt(TILT_HOME)
    time.sleep(0.1)
    
    # Handle cleanup based on hardware type
    if hasattr(pantilthat, 'stop'):
        pantilthat.stop()
    
    time.sleep(1)
    print('Bye ...')

if __name__ == '__main__':
    try:
        # This single line handles auto-detection
        pantilthat = PanTiltController()
        dance()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please ensure PanTilt HAT hardware is connected and I2C is enabled")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)