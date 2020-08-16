pi-shutdown
===========

Shutdown/reboot(/power on) Raspberry Pi with pushbutton

## Usage:

Connect the LCD via I2C to Raspberry Pi and ensure you are able to communicate to it on address 0x27

Connect pushbutton to BCM GPIO pin 23 and ground then run:
```
sudo python pishutdown.py
```

If you have a service you wish to shutxown prior to the Pi rebooting or shutting down, edit the {ServiceNameHere} in both lines to reflect the desired service name.
```
call(['systemctl', 'stop', 'ServiceNameHere'], shell=False)
```

When button is pressed for less than 5 seconds, Pi reboots. If pressed for more than 5 seconds it shuts down.
While shut down, if button is connected to BCM GPIO pin 23, then pressing the button powers on Pi.

## To enable the service on boot run:
```
sudo systemctl enable pishutdown.service
```

## Start/Stop/Restart service:
```
sudo systemctl start pishutdown
sudo systemctl stop pishutdown
sudo systemctl restart pishutdown
```

### View Log Files:
From the directroy you are running pishutdown.sh
```
cat pishutdown.log
```
