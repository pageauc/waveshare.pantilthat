#!/usr/bin/env python
'''
diagnostic.py - Check PanTilt HAT setup
Run this to diagnose hardware detection issues
'''
import sys
import subprocess

def check_i2c_enabled():
    """Check if I2C is enabled in raspi-config"""
    try:
        result = subprocess.run(['lsmod | grep i2c'], shell=True, capture_output=True, text=True)
        if 'i2c_dev' in result.stdout or 'i2c_bcm' in result.stdout:
            return True
    except:
        pass
    return False

def check_i2c_permissions():
    """Check if user has permission to access I2C"""
    try:
        result = subprocess.run(['ls -l /dev/i2c*'], shell=True, capture_output=True, text=True)
        print(f"I2C device permissions:\n{result.stdout}")
        return True
    except:
        return False

def scan_i2c_devices():
    """Scan I2C bus for devices"""
    try:
        result = subprocess.run(['i2cdetect -y 1'], shell=True, capture_output=True, text=True)
        print(f"I2C device scan:\n{result.stdout}")
        return True
    except:
        print("i2cdetect not found. Install with: sudo apt-get install i2c-tools")
        return False

def check_pimoroni_installed():
    """Check if Pimoroni library is installed"""
    try:
        import pantilthat
        print("✓ Pimoroni pantilthat module found")
        print(f"  Module location: {pantilthat.__file__}")
        return True
    except ImportError as e:
        print(f"✗ Pimoroni pantilthat not installed: {e}")
        return False

def main():
    print("=" * 50)
    print("PanTilt HAT Diagnostic Tool")
    print("=" * 50)
    
    # Check I2C
    print("\n1. Checking I2C Configuration:")
    if check_i2c_enabled():
        print("  ✓ I2C appears to be enabled")
    else:
        print("  ✗ I2C may not be enabled")
        print("    Run: sudo raspi-config")
        print("    Then: Interface Options -> I2C -> Enable")
    
    check_i2c_permissions()
    
    # Check user in i2c group
    import os
    import grp
    user = os.getenv('USER')
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    if 'i2c' in groups:
        print(f"  ✓ User '{user}' is in i2c group")
    else:
        print(f"  ✗ User '{user}' is NOT in i2c group")
        print("    Run: sudo usermod -a -G i2c $USER")
        print("    Then: logout and login again")
    
    # Scan I2C bus
    print("\n2. Scanning I2C Bus:")
    scan_i2c_devices()
    
    # Check Pimoroni library
    print("\n3. Checking Pimoroni Library:")
    check_pimoroni_installed()
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. If I2C is not enabled: sudo raspi-config")
    print("2. If not in i2c group: sudo usermod -a -G i2c $USER")
    print("3. If Pimoroni not installed: sudo pip3 install pantilthat")
    print("4. Reboot after making changes: sudo reboot")
    print("=" * 50)

if __name__ == '__main__':
    main()