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

Will Implemented curl install script shortly.
  
 
## pantilthat.py Help
 
pantilthat.py Driver for waveshare pan tilt hat hardware.
This driver uses BCM2835 For Details See http://www.airspayce.com/mikem/bcm2835/
You also need to enable I2C using

    sudo raspi-config
    
Then select Interfaces menu pick, and enable using menu pick ***P5 I2C Enable/Disable automatic loading of I2C kernel module***
    
```
Implementation Example

   from pantilthat import PanTilt # import library
   cam = PanTilt()                # Initialize pantilt servo library
   cam.setPWMFreq(50)             # Optional pwm frequency setting
   cam.setServoPulse(1, 500)      # Optional pwm servo pulse setting
   cam.pan(0)                     # valid values -90 to +90 Move cam horizontally to center position
   cam.tilt(20)                   # valid values -90 to +90 Move cam vertically to slightly above center

Other Options

   cam.__version__()       # Display version Number
   cam.debug = True        # Display additional servo information messages
   cam.flip_servo = False  # Optionally flips pan and tilt in case servo plugin is different
   cam.stop()              # Turn Off pwm to both servo channels
   cam.start()             # Turn On pwm to both servo channels after stop
   cam.help()              # Display this help message

```
