#!/bin/bash

# make sure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root! Try \"sudo ./setup.sh\"" 
   exit 1
fi

# Enable hardware PWM
echo "dtoverlay=pwm-2chan" >> /boot/config.txt
# Enable I2C
raspi-config nonint do_i2c 0

# update software so that we pull the latest packages
apt update -y
apt full-upgrade -y

# install dependencies 
apt install git xvkbd python3 python3-pip python3-pyqt5 python3-numpy -y
pip3 install rpi-hardware-pwm pyqtgraph Adafruit-Blinka adafruit-circuitpython-ads1x15

# get the code from the repo
git clone https://github.com/ECE-492-capstone/spinal-stiffness-indenter

echo "Please reboot with \"sudo reboot\" to finish setup!"
