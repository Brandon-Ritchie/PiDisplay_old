#! /bin/bash

# Update Raspberry Pi
sudo apt update &&
sudo apt upgrade -y &&

# Install dependencies
sudo pip3 install -r /home/pi/Scripts/PiDisplay/requirements.txt
sudo apt install cec-utils -y &&
sudo apt install chromium-chromedriver
