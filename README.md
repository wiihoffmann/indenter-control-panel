# spinal-stiffness-indenter
The codebase for the spinal stiffness indenter done as a computer engineering capstone project.

# Running instructions
1. Enable hardware PWM by adding the following line to the end of ```/boot/config.txt```
   ```
   dtoverlay=pwm-2chan
   ```
2. Enable hardware I2C by running the following command:
   ```
   sudo raspi-config nonint do_i2c 0
   ```
3. Make sure that everything is up to date and reboot:
   ```
   sudo apt update
   sudo apt full-upgrade
   sudo reboot
   ```
4. Install all of the dependencies:
   ```
   sudo apt install git python3-pip python3-pyqt5 python3-numpy python3-matplotlib  
   sudo pip3 install rpi-hardware-pwm pyqtgraph Adafruit-Blinka adafruit-circuitpython-ads1x15
   ```
5. Get the code from this repo:
   ```
   git clone https://github.com/ECE-492-capstone/spinal-stiffness-indenter
   ```
6. Make sure you are in the right directory and run the code:
   ```
   cd spinal-stiffness-indenter
   python3 main.py
   ```
