#!/bin/bash

cd ~
echo "Installing Waveshare python libraries and PWM driver"
wget -O pantilthat.py https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/pantilthat.py

# create python library module folders for python2 and python3
sudo mkdir -p /usr/local/lib/python2.7/dist-packages/waveshare
sudo cp pantilthat.py /usr/local/lib/python2.7/dist-packages/waveshare
sudo touch /usr/local/lib/python2.7/dist-packages/waveshare/__init__.py
sudo mkdir -p /usr/local/lib/python3.7/dist-packages/waveshare
sudo cp pantilthat.py /usr/local/lib/python3.7/dist-packages/waveshare
sudo touch /usr/local/lib/python3.7/dist-packages/waveshare/__init__.py
rm pantilthat.py

echo "Install Python 2 and 3 Dependencies"
sudo apt-get -yq install python-rpi.gpio
sudo apt-get -yq install python3-rpi.gpio

bcm_ver='73'
echo "$0 Install bcm2835-1.$bcm_ver  Please wait ..."
echo "$0 Downloading http://www.airspayce.com/mikem/bcm2835/bcm2835-1.$bcm_ver.tar.gz"
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.$bcm_ver.tar.gz
tar -zxvf bcm2835-1.$bcm_ver.tar.gz
cd bcm2835-1.$bcm_ver
sudo ./configure
echo "$0 Compiling ..... One Moment Please"
sudo make
sudo make check
echo "$0 Running make install"
sudo make install
echo "$0 Performing Cleanup"
cd ~
rm bcm2835-1.$bcm_ver.tar.gz
sudo rm -r  bcm2835-1.$bcm_ver
echo "$0 Completed Install of bcm2835-1.$bcm_ver"
echo "
-----------------------------------------------
Install Complete
-----------------------------------------------
INSTRUCTIONS Assumes you are comfortable with SSH and/or Terminal session commands

1. Ensure waveshare pantilt hardware is assembled and connected to the Raspberry Pi
2. Ensure I2C is Enabled using raspi-config whiptail menu system.

    sudo raspi-config

Using whiptail menu select Interfacing then I2C and Enable.
Optionally you can Enable Pi Camera module support.

Example python script to center pantilthat.
Valid pan and tilt values are between -90 to +90 degrees

    #!/usr/bin/env python
    import time
    import RPi.GPIO as GPIO
    from waveshare.pantilthat import PanTilt
    pantilthat = PanTilt()
    
    pantilthat.pan(0)
    pantilthat.tilt(0)
    time.sleep(0.1)
    pantilthat.stop()
    time.sleep(2) # Allow time for driver to stop
    print('pantilthat at pan=0, tilt=0')
    print('Bye ...')

Good Luck Claude ...
Bye"