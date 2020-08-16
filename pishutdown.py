#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi with pushbutton

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
import lcddriver
import logging
from logging.handlers import RotatingFileHandler

# Setup logging envirioment
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
formatter = logging.Formatter('%(asctime)s,:%(levelname)s:%(name)s,:%(message)s')
file_handler = logging.FileHandler('pishutdown.log')
file_handler.setFormatter(formatter)
handler = RotatingFileHandler('pishutdown.log', maxBytes=10000, backupCount=5)
logger.addHandler(file_handler)

logger.info("pishutdown service started")

# pushbutton connected to this BCM GPIO pin, using pin 23 also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 23

# if button pressed for at least this long then shut down. if less then reboot.
shutdownMinSeconds = 5

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None

# Set varable to call the lcd driver and clear the screen.
lcd = lcddriver.lcd()

def buttonStateChanged(pin):
    global logger
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # button is down
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        # button is up
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= shutdownMinSeconds:
                logger.warning("Shutdown initiated")
                time.sleep(1)
                lcd.lcd_clear()
                time.sleep(0.5)
                lcd.lcd_display_string("Shutting down...    ", 1)
                # button pressed for more than specified time, shutdown
                # Stop service before shutdown
                call(['systemctl', 'stop', 'ServiceNameHere'], shell=False)
                time.sleep(5)
                #turn off backlight
                lcd.lcd_clear()
                time.sleep(0.5)
                lcd.lcd_backlight("off")
                logger.info("LCD backlight off.")
                call(['shutdown', '-h', 'now'], shell=False)
            elif elapsed >= debounceSeconds:
                logger.warning("Reboot initiated")
                time.sleep(1)
                lcd.lcd_clear()
                time.sleep(0.5)
                lcd.lcd_display_string("Rebooting...        ", 1)
                # button pressed for a shorter time, reboot
                # Stop service before shutdown
                call(['systemctl', 'stop', 'ServiceNameHere'], shell=False)
                time.sleep(5)
                call(['shutdown', '-r', 'now'], shell=False)



# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
    # sleep to reduce unnecessary CPU usage
    time.sleep(5)
