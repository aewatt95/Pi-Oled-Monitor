#!/usr/bin/env python

import time
import os
import psutil
import sys
import subprocess
import signal
from collections import deque
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

interface = "wlan0"

#Change to spi(...) instead of i2c(...) if your SSD1306 is controlled by SPI
serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)

runAllowed = True

font_path = ""
icon = ImageFont.truetype(font_path + "MaterialIcons-Regular.ttf", 15)

def endReceive(a, b):
	global runAllowed
	runAllowed = False

signal.signal(signal.SIGINT, endReceive)
signal.signal(signal.SIGTERM, endReceive)

tmpUpMax = 1.0
tmpDownMax = 1.0

netBufUp = deque(maxlen=10)
netBufDown = deque(maxlen=10)

while runAllowed:
	#Get information from proc
	cmdUp = "sudo cat /proc/net/dev | awk 'NR==0; END{print}' | awk '{print $10}'"
	cmdDown = "sudo cat /proc/net/dev | awk 'NR==0; END{print}' | awk '{print $2}'"
	sUp = subprocess.Popen(cmdUp, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0][:-1]
	sDown = subprocess.Popen(cmdDown, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0][:-1]

	try:
		float(sUp)
		float(sDown)
	except ValueError:
		sUp = "0"
		sDown = "0"
	netBufUp.append(int(sUp))
	netBufDown.append(int(sDown))

	#Get raw Data [float]
	#Change / to /media/YOURDEVICE if you want to monitor an external USB device
	rawUsage = psutil.disk_usage('/').percent
	rawNet = float(sUp)
	rawMem = psutil.virtual_memory().percent
	rawCpu = psutil.cpu_percent(interval=None)

	formNetUp = float(netBufUp[-1]-netBufUp[0])
	formNetDown = float(netBufDown[-1]-netBufDown[0])

	if formNetUp > tmpUpMax:
		tmpUpMax = formNetUp

	if formNetDown > tmpDownMax:
		tmpDownMax = formNetDown

	formUsage = round(rawUsage/100, 3)
	formNet = int(round(rawNet))
	formMem = round(rawMem/100.0, 3)
	formCpu = rawCpu/100.0

	with canvas(device) as draw:
		draw.rectangle([20,2,118,12],None, 1)
		draw.rectangle([20,18,118,28],None, 1)
		draw.rectangle([20,34,64,44],None, 1)
		draw.rectangle([70,34,118,44],None, 1)
		draw.rectangle([20,50,118,60],None, 1)

		draw.text((0,0),text=u'\ue8b8', font=icon, fill="white")
		draw.text((0,16),text=u'\ue322', font=icon, fill="white")
		draw.text((0,32),text=u'\ue0c3', font=icon, fill="white")
		draw.text((0,48),text=u'\ue623', font=icon, fill="white")

		draw.rectangle([20,2,20+(formCpu*98),12], fill="white", width=1)
		draw.rectangle([20,18,20+(formMem*98),28], fill="white", width=1)
		draw.rectangle([20,34,20+((formNetUp/tmpUpMax)*44),44], fill="white", width=1)
		draw.rectangle([70,34,70+((formNetDown/tmpDownMax)*48),44], fill="white", width=1)
		draw.rectangle([20,50,20+(formUsage*98),60],fill="white", width=1)
	time.sleep(0.1)
