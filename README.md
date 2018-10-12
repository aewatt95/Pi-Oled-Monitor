This script is used to show system resource informations on an SSD1306 OLED display.

![Oled Display](https://cdn.thingiverse.com/renders/c3/b7/d5/c0/e1/68b8da18b966ef9e4dee565c13fb22a6_preview_featured.jpg)

## Requirements
+ Python 2.7
+ Luma core library 
+ Luma oled library 
+ Pillow

```bash
sudo apt install python python-pip
sudo pip install pillow luma.core luma.oled psutil
```

## Hardware
The Display is connected to the default I2C port on the [Raspberry Pi Header](https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/)
```
VCC -> Pin 1
GND -> Pin 6
SDA -> Pin 3
SCL -> Pin 5
```
It's also possible to use an spi based OLED. Take a look in the main script and modify the marked line.

## Installation
Use ```sudo chmod +x watchOLED_change.py``` to make the script executable
and ```sudo ./watchOLED_change.py``` to run the script


## Autostart
If you want to enable autostart, open the .service file and change
```/PATH/TO/SCRIPTDIRECTORY``` to your actual working directory 

Add the .service file to your boot routine
```bash
sudo cp oledMonitor.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable oledMonitor.service
```
