"""
Imports
"""
from utilities import print_with_time, assign_display_text # Utilities for Display Stuff
from state import state # importing state to tell whether to turn on or switch
from selenium import webdriver # selenium for Web Driving
import pyautogui # pyautogui for moving the mouse
from models import DisplayEntry
from app import db

if __name__ == '__main__':
    display_text = assign_display_text(state, db.session.query(DisplayEntry).order_by(DisplayEntry.id).all()) # Get day of the week and assign variable

    # Set up webdriver and open page
    print_with_time('Setting up browser')
    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_argument("--disable-infobars")                                            # remove info bars from top of chrome
    chromeoptions.add_argument("--kiosk")                                                       # enable kiosk mode
    chromeoptions.add_experimental_option('excludeSwitches', ["enable-automation"])             # disable automation warning
    chromeoptions.add_experimental_option('useAutomationExtension', False)                      # disable automation warning
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', 0, chromeoptions)       # set up driver variable
    driver.implicitly_wait(10)                                                                  # try each thing for 10 seconds
    print_with_time('Opening displays website')
    driver.get('https://stambaughauditorium.com/sa-displays')                                   # open displays website

    # Open correct link
    print_with_time('Clicking on specified display link')
    link = driver.find_element_by_link_text(display_text)
    link.click()

    # Move mouse from center of screen
    print_with_time('Getting gui size')
    screen_size = pyautogui.size()
    print_with_time('Moving mouse to the corner of the screen')
    pyautogui.moveTo(screen_size[0]-1,screen_size[1]-1)