# waveshare.pantilthat
#### WaveShare pan tilt hat python library class and demo for Raspberry Pi

I bought the waveshare pan tilt hat for a Raspberry Pi project I was working on.
I found Assembly tricky but with the help of a [YouTube video](https://www.youtube.com/watch?v=4A7tJ0QH4L4) I got it together.
I felt the [vendor instructions]( https://www.waveshare.com/pan-tilt-hat.htm) and 
[GitHub Repo](https://github.com/waveshare/Pan-Tilt-HAT) were lacking, especially the python library.
I wrote my own python library that is similar to the Pimoroni pan tilt hat operation that uses -90 to +90 values for the pan and tilt
positions. I also have several Pimoroni pan tilt hats and found support was much better and trouble free. 
Below is the driver help instructions. I also wrote a comprehensive demo python script.

## Quick Install

IMPORTANT - It is suggested you do a Raspbian sudo apt-get update and sudo apt-get upgrade before curl install.

Step 1 With mouse left button highlight curl command in code box below. Right click mouse in highlighted area and Copy.
Step 2 On RPI putty SSH or terminal session right click, select paste then Enter to download and run script.

    curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/master/install.sh | bash

This will create a /home/pi/waveshare folder and required files for testing the waveshare pantilt hardware
  
 
## Instructions
 
The ***pantilthat.py*** file is the python class library for waveshare pan tilt hat hardware.
This driver uses BCM2835 and I2C. For Details See http://www.airspayce.com/mikem/bcm2835/

You also need to ***enable I2C***    
From a Logged in SSH or Terminal session on the Raspbery Pi. Run the
Raspberry PI configuration whiptail menu per command below

    sudo raspi-config
    
Select ***5 Interfacing Options*** menu pick         
Then select ***P5 I2C*** menu pick and Enable automatic loading of I2C kernel module
 
Reboot and run the example ***test-pantilt.py*** demo python script.

    sudo apt install python-picamera
    
    cd ~/waveshare
    python ./test-pantilt.py

Press ctrl-c to exit script

### pantilthat.py help() 
```
Implementation Example

   from pantilthat import PanTilt # import library
   cam = PanTilt()                # Initialize pantilt servo library
   cam.setPWMFreq(50)             # Default=50 Optional pwm frequency setting
   cam.setServoPulse(1, 500)      # Optional pwm servo pulse setting
   cam.pan(0)                     # valid values -90 to +90 Move cam horizontally to center position
   cam.tilt(20)                   # valid values -90 to +90 Move cam vertically to slightly above center

Other Options

   cam.__version__()       # Display version Number
   cam.debug = False       # True= Display additional servo information messages
   cam.flip_servo = False  # True= Optionally flips pan and tilt in case servo plugin is different
   cam.stop()              # Turn Off pwm to both servo channels
   cam.start()             # Turn On pwm to both servo channels after stop
   cam.help()              # Display this help message

```
