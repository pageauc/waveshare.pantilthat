#!/usr/bin/python
'''
Enhanced driver for waveshare/pimoroni pantilthat with auto-detection
Compatible with both hardware types using unified interface
Optimized for Raspberry Pi OS Bookworm
'''
import time
import math
import sys
import warnings
import os
import subprocess

# Global flags for hardware detection
PIMORONI_AVAILABLE = False
PIMORONI_WORKING = False
pimoroni_pantilthat = None
SMBUS_AVAILABLE = False

# Try multiple methods to import Pimoroni
try:
    import pantilthat as pimoroni_pantilthat
    if hasattr(pimoroni_pantilthat, 'pan'):
        PIMORONI_AVAILABLE = True
        print("Found system pantilthat package")
        
        # Test Pimoroni hardware if available
        try:
            # Try to initialize the hardware
            if hasattr(pimoroni_pantilthat, '__version__'):
                print(f"Pimoroni library version: {pimoroni_pantilthat.__version__}")
            
            # Some Pimoroni versions need explicit initialization
            if hasattr(pimoroni_pantilthat, 'init'):
                pimoroni_pantilthat.init()
            
            # Try a simple command
            pimoroni_pantilthat.pan(0)
            pimoroni_pantilthat.tilt(0)
            time.sleep(0.1)
            PIMORONI_WORKING = True
            print("Pimoroni hardware communication successful")
        except Exception as e:
            print(f"Pimoroni hardware communication failed: {e}")
            PIMORONI_WORKING = False
except ImportError:
    pass

# Import smbus for Waveshare
try:
    import smbus
    SMBUS_AVAILABLE = True
except ImportError:
    SMBUS_AVAILABLE = False

class PanTiltController:
    """Unified PanTilt controller that auto-detects hardware"""
    
    def __new__(cls, *args, **kwargs):
        """Auto-detect which hardware is available"""
        # Try Pimoroni first if it's working
        if PIMORONI_AVAILABLE and PIMORONI_WORKING:
            print("Using Pimoroni PanTilt HAT")
            return PimoroniWrapper()
        
        # If Pimoroni is installed but not working, try Waveshare
        if PIMORONI_AVAILABLE and not PIMORONI_WORKING:
            print("Pimoroni library found but hardware not responding")
            print("Attempting to use Waveshare driver...")
        
        # Fall back to Waveshare
        if SMBUS_AVAILABLE:
            try:
                # Test Waveshare communication
                bus = smbus.SMBus(1)
                # Try to read from the device
                bus.read_byte(0x40)
                # Create and return Waveshare instance
                instance = super().__new__(cls)
                print("Using Waveshare PanTilt HAT")
                return instance
            except Exception as e:
                print(f"Waveshare hardware test failed: {e}")
        
        # If we get here, no hardware is working
        error_msg = []
        if not PIMORONI_AVAILABLE:
            error_msg.append("Pimoroni module not available")
        if PIMORONI_AVAILABLE and not PIMORONI_WORKING:
            error_msg.append("Pimoroni hardware not responding")
        if not SMBUS_AVAILABLE:
            error_msg.append("smbus module not available for Waveshare")
        
        raise ImportError("No working PanTilt HAT hardware detected:\n  " + 
                        "\n  ".join(error_msg))
    
    def __init__(self, address=0x40, debug=False):
        """Initialize Waveshare hardware"""
        # This will only be called for Waveshare instances
        self.__SUBADR1 = 0x02
        self.__SUBADR2 = 0x03
        self.__SUBADR3 = 0x04
        self.__MODE1 = 0x00
        self.__MODE2 = 0x01
        self.__PRESCALE = 0xFE
        self.__LED0_ON_L = 0x06
        self.__LED0_ON_H = 0x07
        self.__LED0_OFF_L = 0x08
        self.__LED0_OFF_H = 0x09
        self.__ALLLED_ON_L = 0xFA
        self.__ALLLED_ON_H = 0xFB
        self.__ALLLED_OFF_L = 0xFC
        self.__ALLLED_OFF_H = 0xFD
        
        self.prog_ver = '0.9'
        self.pan_servo = 0
        self.tilt_servo = 1
        self.flip_servo = False
        self.address = address
        self.debug = debug
        self._initialized = False
        self._setup_hardware()
    
    def _setup_hardware(self):
        """Setup Waveshare hardware"""
        try:
            self.bus = smbus.SMBus(1)
            self.setPWMFreq(50)
            self.setServoPulse(1, 500)
            self.write(self.__MODE1, 0x00)
            self._initialized = True
        except Exception as e:
            raise IOError(f"Failed to initialize Waveshare hardware: {e}")
    
    def write(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        try:
            self.bus.write_byte_data(self.address, reg, value)
            if self.debug:
                print(f"I2C: Write 0x{value:02X} to register 0x{reg:02X}")
        except Exception as e:
            raise IOError(f"Failed to write to I2C device: {e}")

    def read(self, reg):
        """Read an unsigned byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if self.debug:
                print(f"I2C: Device 0x{self.address:02X} returned 0x{result:02X} from reg 0x{reg:02X}")
            return result
        except Exception as e:
            raise IOError(f"Failed to read from I2C device: {e}")

    def setPWMFreq(self, freq=50):
        """Sets the PWM frequency"""
        prescaleval = 25000000.0 / 4096.0 / float(freq) - 1.0
        prescale = math.floor(prescaleval + 0.5)
        
        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.write(self.__MODE1, newmode)
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)
        self.write(self.__MODE2, 0x04)

    def setPWM(self, channel, on, off):
        """Sets a single PWM channel"""
        self.write(self.__LED0_ON_L + 4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4*channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4*channel, off >> 8)

    def setServoPulse(self, channel=1, pulse=5000):
        """Sets the Servo Pulse, The PWM frequency must be 50HZ"""
        pulse = pulse * 4096 / 20000
        self.setPWM(channel, 0, int(pulse))

    def setRotationAngle(self, channel, angle):
        """Set servo rotation angle"""
        angle = angle + 90
        if 0 <= angle <= 180:
            temp = angle * (2000 / 180) + 501
            self.setServoPulse(channel, temp)
        else:
            print(f"Angle {angle-90} is Out of Range must be between -90 and +90")

    def pan(self, angle):
        """Pan Left and Right with Left = -90 and Right = 90"""
        angle = max(-90, min(90, angle))
        if self.flip_servo:
            self.setRotationAngle(self.tilt_servo, angle)
        else:
            self.setRotationAngle(self.pan_servo, angle)

    def tilt(self, angle):
        """Tilt Up and Down with Up = -90 and Down = 90"""
        angle = max(-90, min(90, angle))
        if self.flip_servo:
            self.setRotationAngle(self.pan_servo, angle)
        else:
            self.setRotationAngle(self.tilt_servo, angle)

    def start(self):
        """Start PWM output"""
        if hasattr(self, 'bus'):
            self.write(self.__MODE2, 0x04)

    def stop(self):
        """Stop PWM output"""
        if hasattr(self, 'bus'):
            self.write(self.__MODE2, 0x00)

    def help(self):
        """Display help"""
        print('=' * 50)
        print('Unified PanTilt HAT Driver v' + self.prog_ver)
        print('=' * 50)
        print('\nUsage:')
        print('  from waveshare.pantilthat import PanTiltController')
        print('  pt = PanTiltController()')
        print('  pt.pan(0)    # Center')
        print('  pt.tilt(0)   # Center')
        print('\n' + str(get_hardware_info()))


class PimoroniWrapper:
    """Wrapper class to make Pimoroni module behave like our class"""
    
    def __init__(self):
        global PIMORONI_WORKING, pimoroni_pantilthat
        self._module = pimoroni_pantilthat
        self.prog_ver = '0.9 (Pimoroni)'
        self.flip_servo = False
        self._working = PIMORONI_WORKING
        
        if not self._working:
            print("WARNING: Pimoroni hardware not responding")
    
    def pan(self, angle):
        """Forward pan call to Pimoroni module"""
        if not self._working:
            print("Error: Pimoroni hardware not available")
            return
        try:
            self._module.pan(angle)
        except Exception as e:
            print(f"Pimoroni pan error: {e}")
            self._working = False
    
    def tilt(self, angle):
        """Forward tilt call to Pimoroni module"""
        if not self._working:
            print("Error: Pimoroni hardware not available")
            return
        try:
            self._module.tilt(angle)
        except Exception as e:
            print(f"Pimoroni tilt error: {e}")
            self._working = False
    
    def start(self):
        pass
    
    def stop(self):
        """Disable servos if possible"""
        try:
            if hasattr(self._module, 'servo_enable'):
                self._module.servo_enable(0, False)
                self._module.servo_enable(1, False)
        except:
            pass
    
    def help(self):
        print("Pimoroni PanTilt HAT")
        print("Status: " + ("Working" if self._working else "Not responding"))
    
    def __version__(self):
        return self.prog_ver


def get_hardware_info():
    """Return information about detected hardware"""
    info = {"type": "None", "status": "Not detected"}
    
    if PIMORONI_AVAILABLE:
        info["type"] = "Pimoroni"
        info["status"] = "Working" if PIMORONI_WORKING else "Not responding"
        info["module"] = "system package"
    
    if SMBUS_AVAILABLE and (not PIMORONI_AVAILABLE or not PIMORONI_WORKING):
        try:
            bus = smbus.SMBus(1)
            bus.read_byte(0x40)
            info["type"] = "Waveshare"
            info["status"] = "Working"
            info["address"] = "0x40"
        except Exception as e:
            info["type"] = "Waveshare"
            info["status"] = f"I2C communication failed: {e}"
    
    return info


def is_available():
    """Check if any PanTilt hardware is available and working"""
    if PIMORONI_AVAILABLE and PIMORONI_WORKING:
        return True
    
    if SMBUS_AVAILABLE:
        try:
            bus = smbus.SMBus(1)
            bus.read_byte(0x40)
            return True
        except:
            return False
    
    return False


# For backward compatibility
class PanTilt(PanTiltController):
    """Alias for PanTiltController for backward compatibility"""
    def __init__(self, *args, **kwargs):
        warnings.warn("PanTilt class is deprecated. Use PanTiltController.", DeprecationWarning)
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    print("Testing PanTilt HAT detection...")
    print(f"Python environment: {sys.prefix}")
    info = get_hardware_info()
    print(f"Hardware: {info['type']} - {info['status']}")
    
    if is_available():
        print("\nCreating PanTiltController instance...")
        pt = PanTiltController()
        
        print("Testing movement...")
        pt.pan(0)
        pt.tilt(0)
        time.sleep(1)
        
        print("Sweep test...")
        for angle in range(-90, 91, 45):
            print(f"Moving to {angle}")
            pt.pan(angle)
            pt.tilt(angle)
            time.sleep(0.5)
        
        pt.pan(0)
        pt.tilt(0)
        time.sleep(1)
        
        if hasattr(pt, 'stop'):
            pt.stop()
        
        print("Test complete!")
    else:
        print("\nNo working PanTilt hardware detected.")