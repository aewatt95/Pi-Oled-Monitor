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

Autostart

If you want to enable autostart, open the .service file and change
```/PATH/TO/SCRIPTDIRECTORY``` to your actual working directory 
