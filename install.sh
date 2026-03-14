#!/bin/bash

ver="0.8"

INSTALL_DIR='waveshare'  # Default folder install location

cd ~
mkdir -p $INSTALL_DIR

# Remember where this script was launched from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $INSTALL_DIR
INSTALL_PATH=$( pwd )
echo "-----------------------------------------------"
echo "$STATUS install.sh ver $ver"
echo "-----------------------------------------------"
echo "$STATUS Download GitHub Files"
installFiles=("pantilthat.py" "test-pantilt.py" "sinewave-dance.py" "waveshare.txt" "README.md" "LICENCE" "pantilt_diagnose.py")
for fname in "${installFiles[@]}" ; do
    wget_output=$(wget -O $fname -q --show-progress https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/$fname)
    if [ $? -ne 0 ]; then
        if [ $? -ne 0 ]; then
            echo "ERROR - $fname wget Download Failed. Possible Cause Internet Problem."
        else
            wget -O $fname https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/$fname
        fi
    fi
done

PYTHON_VERSION=$(python3 -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
sudo mkdir -p /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare
sudo cp pantilthat.py /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare
sudo touch /usr/local/lib/$PYTHON_VERSION/dist-packages/waveshare/__init__.py
rm pantilthat.py

chmod +x *py

echo "$STATUS Install Dependencies"
sudo apt-get -yq install python3-rpi.gpio
sudo apt-get -yq install python3-picamera2

echo "
-----------------------------------------------
$STATUS Complete
-----------------------------------------------
INSTRUCTIONS Assumes you are comfortable with SSH and/or Terminal session commands

1. Ensure picamera module is enabled, connected and working.
2. Ensure waveshare pantilt hardware is assembled and connected to the Raspberry Pi
3. Ensure I2C and picamera are Enabled using raspi-config whiptail menu system.

    sudo raspi-config

Using whiptail menu select Interfacing then I2C and Enable.
Also ensure the picamera module is Enabled.

4. Reboot RPI

5. Run demo per the following commands

    cd ~/waveshare
    ./test-pantilt.py
    ./sinewave-dance.py

Good Luck Claude ...
Bye"
