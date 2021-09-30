#! /bin/bash

# Update Raspberry Pi
sudo apt update &&
sudo apt upgrade -y &&

# Make Scripts Directory and copy scripts
mkdir /home/pi/Scripts &&
git clone https://github.com/Brandon-Ritchie/PiDisplay.git /home/pi/Scripts/PiDisplay &&

# Install dependencies
sudo pip3 install Flask-WTF &&
sudo pip3 install Flask-SQLAlchemy &&
sudo pip3 install python-crontab &&
sudo pip3 install flask-login &&
sudo pip3 install werkzeug &&
pip3 install selenium &&
pip3 install PyAutoGui &&
sudo apt install cec-utils -y &&
sudo apt install chromium-chromedriver
