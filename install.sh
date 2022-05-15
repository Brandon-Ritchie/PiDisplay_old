#! /bin/bash

# Update Raspberry Pi
sudo apt update &&
sudo apt upgrade -y &&

# Make Scripts Directory and copy scripts
mkdir /home/pi/Scripts &&
git clone https://github.com/Brandon-Ritchie/PiDisplay.git /home/pi/Scripts/PiDisplay &&

# Install dependencies
sudo pip3 install -r requirements.txt
sudo apt install cec-utils -y &&
sudo apt install chromium-chromedriver
