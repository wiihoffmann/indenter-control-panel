#!/bin/bash

# make sure script is run as root
#if [[ $EUID -ne 0 ]]; then
#   echo "This script must be run as root! Try \"sudo ./setup.sh\"" 
#   exit 1
#fi

# update software so that we pull the latest packages
sudo apt update -y
sudo apt full-upgrade -y

# install dependencies 
sudo apt install git onboard python3 python3-pip python3-pyqt5 python3-numpy python3-pyqtgraph -y

# auto launch onboard
mkdir ~/.config/autostart
echo "[Desktop Entry]" > ~/.config/autostart/keyboard.desktop
echo "Type=Application" >> ~/.config/autostart/keyboard.desktop
echo "Name=onboard" >> ~/.config/autostart/keyboard.desktop
echo "Exec=onboard" >> ~/.config/autostart/keyboard.desktop

echo "[Desktop Entry]" > ~/.config/autostart/xpresso.desktop
echo "Type=Application" >> ~/.config/autostart/xpresso.desktop
echo "Name=Xpresso Controls" >> ~/.config/autostart/xpresso.desktop
echo "Exec=indenter-control-panel/Main.py" >> ~/.config/autostart/xpresso.desktop

echo "Please reboot with \"sudo reboot\" to finish setup!"
