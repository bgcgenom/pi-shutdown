pi-shutdown
===========

Shutdown/reboot(/power on) Raspberry Pi with pushbutton

## Usage:
Connect pushbutton to BCM GPIO pin 23 and ground then run:
```
sudo python pishutdown.py
```

When button is pressed for less than 5 seconds, Pi reboots. If pressed for more than 5 seconds it shuts down.
While shut down, if button is connected to BCM GPIO pin 23, then pressing the button powers on Pi.

To enable the service run:
```
sudo systemctl enable pishutdown.service
```
