# spinal-stiffness-indenter
The codebase for the spinal stiffness indenter done as a computer engineering capstone project.

# Setup instructions (quick)
1. Get the code from this repo and cd into the directory:
   ```
   git clone https://github.com/wiihoffmann/spinal-stiffness-indenter
   cd spinal-stiffness-indenter
   ```
2. Run the setup script:
   ```
   sudo ./setup.sh
   ```
3. Enable the RTC module with the following commands:
   ```
   sudo modprobe rtc-ds1307
   sudo echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
   sudo hwclock -w
   ```
   Add the following lines to ```/etc/rc.local``` above the ```exit 0``` line at the bottom to enable the RTC at boot.
   ```
   echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
   sudo hwclock -s
   date
   ```
4. Run the program:
   ```
   ./Main.py
   ```

# Setup instructions (full)
1. Enable hardware PWM by adding the following line to the end of ```/boot/config.txt```
   ```
   dtoverlay=pwm-2chan
   ```
2. Enable hardware I2C by running the following command:
   ```
   sudo raspi-config nonint do_i2c 0
   ```
3. Enable the RTC module with the following commands:
   ```
   sudo modprobe rtc-ds1307
   sudo echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
   sudo hwclock -w
   ```
   Add the following lines to ```/etc/rc.local``` above the ```exit 0``` line at the bottom to enable the RTC at boot.
   ```
   echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
   sudo hwclock -s
   date
   ```
4. Make sure that everything is up to date and reboot:
   ```
   sudo apt update
   sudo apt full-upgrade
   sudo reboot
   ```
5. Install all of the dependencies:
   ```
   sudo apt install git xvkbd python3 python3-pip python3-pyqt5 python3-numpy
   sudo pip3 install rpi-hardware-pwm pyqtgraph Adafruit-Blinka adafruit-circuitpython-ads1x15
   ```
6. Get the code from this repo:
   ```
   git clone https://github.com/ECE-492-capstone/spinal-stiffness-indenter
   ```
7. Make sure you are in the right directory and run the code:
   ```
   cd spinal-stiffness-indenter
   python3 main.py
   ```
