#!/bin/bash
ver='68'
cd ~
echo "$0 Install bcm2835-1.$ver  Please wait"
echo "$0 Downloading http://www.airspayce.com/mikem/bcm2835/bcm2835-1.$ver.tar.gz"
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.$ver.tar.gz
tar -zxvf bcm2835-1.$ver.tar.gz 
cd bcm2835-1.$ver
sudo ./configure
echo "$0 Compiling ..... One Moment Please"
sudo make
sudo make check
echo "$0 Running make install"
sudo make install
echo "$0 Performing Cleanup"
cd ~
rm bcm2835-1.$ver.tar.gz
sudo rm -r  bcm2835-1.$ver
echo "$0 Completed Intall of bcm2835-1.$ver"
