# waveshare.pantilthat
### Unified Python Library for Waveshare & Pimoroni Pan-Tilt HATs on Raspberry Pi

This repository provides a **unified Python driver** for both **Waveshare Pan-Tilt HAT** and **Pimoroni Pan-Tilt HAT** hardware. The driver automatically detects which HAT is connected, offering a single, simple interface for your projects.

I initially created this for the Waveshare HAT due to limited vendor support, drawing inspiration from the excellent Pimoroni library. Now, it seamlessly supports both!

**Key Features:**
*   **Auto-Detection:** One import, one interface. Works with Waveshare *or* Pimoroni hardware without code changes.
*   **Simple API:** Uses intuitive `pan(angle)` and `tilt(angle)` commands with values from `-90` to `+90` (0 = center).
*   **Cross-Platform:** Tested on Raspberry Pi OS (including Bookworm) with Python 3.
*   **Demos Included:** Get started quickly with example scripts.


## 🚀 Quick Install (Recommended)

**Prerequisite:** Ensure your system is updated.

    sudo apt-get update && sudo apt-get upgrade -y

### Step 1: Install the driver and demos with a single command:

copy appropriate curl command by pressing the github copy icon on right of code box then paste into SSH or terminal session on RPI

install.sh creates a ~/waveshare folder with all necessary Unified python librsry files, Demo and information files.

    curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/install.sh | bash

install-driver.sh installs only the pantilthat Unified python3 library without demo files

    curl -L https://raw.githubusercontent.com/pageauc/waveshare.pantilthat/main/install-driver.sh | bash	
	

### Step 2: Enable I2C (if not already done):

    sudo raspi-config

Navigate to Interface Options -> I2C -> Enable. Reboot your Pi.

### Step 3: Run a demo!

    cd ~/waveshare
    python3 sinewave-dance.py

The script will auto-detect your HAT and start a smooth sine wave movement. Press Ctrl-C to exit.

## Solutions for Pimoroni on Bookworm or later:
### Option 1: Use the System Package (Recommended)

    sudo apt install python3-pantilthat

### Option 2: Create a Virtual Environment (Works with pip)
    If you need to run your project in a python virtual envionment

    cd ~/waveshare
    python3 -m venv pantilt-env --system-site-packages

    # Activate it
    source pantilt-env/bin/activate

    # Installing Pimoroni pantilt using pip works inside the venv
    pip install pantilthat

    # Run your script
    python sinewave-dance.py

To exit the python environment from within the env

    deactivate

## Usage Examples
Using the unified driver is straightforward. Here's how you use it in your own projects after installation.

### Basic Control

    python3
    from waveshare.pantilthat import PanTiltController

    # Auto-detects your hardware (Waveshare or Pimoroni)
    pt = PanTiltController()

    # Center the servos
    pt.pan(0)
    pt.tilt(0)

    # Move pan 45 degrees right, tilt 30 degrees up
    pt.pan(45)
    pt.tilt(-30)  # Note: Up is often negative

### Advanced (Waveshare-Specific Settings)
For Waveshare hardware, you can access additional configuration options.

    python3
    from waveshare.pantilthat import PanTiltController

    pt = PanTiltController(debug=True)   # Enable debug messages
    pt.flip_servo = True                 # Swap pan and tilt servos if needed
    pt.setPWMFreq(50)                    # Adjust PWM frequency
    # ... control pan/tilt as usual ...
    pt.stop()                            # Turn off PWM output

### Check Hardware Status

    python3
    from waveshare.pantilthat import get_hardware_info, is_available

    if is_available():
        info = get_hardware_info()
        print(f"Detected: {info['type']} - {info['status']}")

## Included Demo Scripts
After installation, explore these scripts in the ~/waveshare folder:

### Script Description

    test-pantilt.py	Interactive menu to manually test pan, tilt, and camera functions.

    sinwave-dance.py	Makes the servos perform a smooth, mesmerizing sine wave dance.

    diagnostic.py	A utility to check I2C, permissions, and hardware detection. Run with python3 diagnostic.py.

## Detailed Documentation
For a deeper dive into the driver's functions, hardware-specific notes, and troubleshooting tips,
please see the included waveshare.txt file in the repository. It contains the complete help text from the driver.

## Contributing & Support
Found a bug? Please open an issue on GitHub.

Have a question? Join the Gitter community chat.

Contributions via pull requests are welcome.

Enjoy your Pan-Tilt projects!