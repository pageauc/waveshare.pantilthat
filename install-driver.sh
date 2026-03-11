#!/bin/bash

cd ~
echo "Installing Waveshare python libraries and PWM driver"
wget -O pantilthat.py https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/pantilthat.py

# create python library module folders for python2 and python3

PYTHON_VERSION=$(python3 -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
sudo mkdir -p /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare
sudo cp pantilthat.py /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare
sudo touch /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare/__init__.py
rm pantilthat.py

echo "Install Python 3 Dependencies"
sudo apt-get -yq install python3-rpi.gpio

-----------------------------------------------
Install Complete
-----------------------------------------------
INSTRUCTIONS Assumes you are comfortable with SSH and/or Terminal session commands

1. Ensure waveshare pantilt hardware is assembled and connected to the Raspberry Pi
2. Ensure I2C is Enabled using raspi-config whiptail menu system.

    sudo raspi-config

Using whiptail menu select Interfacing then I2C and Enable.
Optionally you can Enable Pi Camera module support (legacy).

Example python script to center pantilthat.
Valid pan and tilt values are between -90 to +90 degrees

    #!/usr/bin/env python
    import time
    import RPi.GPIO as GPIO
    from waveshare import PanTilt
    pantilthat = PanTilt()
    pantilthat.setPWMFreq(50)   
    # center pantilt
    pantilthat.pan(0)
    pantilthat.tilt(0)
    time.sleep(0.1) # allow time for servo movement
    pantilthat.stop()
    time.sleep(2) # Allow time for driver to stop
    print('pantilthat centered at pan=0, tilt=0')
    print('Bye ...')

Good Luck Claude ...
Bye"