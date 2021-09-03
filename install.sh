#! /bin/bash

# Update Raspberry Pi
sudo apt update &&
sudo apt upgrade

# Make Scripts Directory and copy scripts
mkdir /home/pi/Scripts &&
git clone https://github.com/LaTromba/PiDisplay.git /home/pi/Scripts/PiDisplay &&

# Install dependencies - seeing if virtual enviroment will cover this
sudo pip3 install Flask-WTF
sudo pip3 install Flask-SQLAlchemy
sudo pip3 install python-crontab
pip3 install selenium
pip3 install pyautogui

# Move desktop startup file to /etc/xdg/autostart
echo "[Desktop Entry]" >> /etc/xdg/autostart/display.desktop &&
echo "sudo python3 /home/pi/Scripts/PiDisplay/app.py" >> /etc/xdg/autostart/display.desktop