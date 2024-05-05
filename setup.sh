#!/bin/bash

# make sure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root! Try \"sudo ./setup.sh\"" 
   exit 1
fi

# update software so that we pull the latest packages
apt update -y
apt full-upgrade -y

# install dependencies 
apt install git xvkbd python3 python3-pip python3-pyqt5 python3-numpy python3-pyqtgraph -y

# get the code from the repo
git clone https://github.com/ECE-492-capstone/spinal-stiffness-indenter

echo "Please reboot with \"sudo reboot\" to finish setup!"
