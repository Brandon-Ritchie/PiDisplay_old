#! /bin/bash

# Update Raspberry Pi
sudo apt update &&
sudo apt upgrade

# Make Scripts Directory and copy scripts
mkdir /home/pi/Scripts &&
git clone https://github.com/LaTromba/PiDisplay.git /home/pi/Scripts/PiDisplay &&

# Install dependencies
sudo pip3 install Flask-WTF &&
sudo pip3 install Flask-SQLAlchemy &&
sudo pip3 install python-crontab &&
pip3 install selenium &&
pip3 install PyAutoGui &&
sudo apt install cec-utils -y &&
sudo apt install chromium-chromedriver