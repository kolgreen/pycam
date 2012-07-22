#!/usr/bin/env python

import sys, os
import cv
from mod_python import util
import time
import serial

#Config
IMG_PATH = "/var/www/camera/"
IMG_NAME = time.strftime("%y%j%H%M%S", time.gmtime())


try:
   ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
   )
except:
   0

def RS(cmd):
	ser.open()
	ser.isOpen()
	ser.write('c')
	time.sleep(1)
	ser.write('2')
	time.sleep(1)
	ser.write(cmd)
	ser.close()


def capture():
	os.system('rm *.jpg -f')

	pt1 = (2,20)
	line_type = cv.CV_AA
        font = cv.InitFont(2, 2 * 0.05 + 0.01, 20 * 0.05 + 0.01, 2 * 0.1, 1, line_type)	

	try:
		pCI = cv.CaptureFromCAM(-1)
		#rospy.sleep(0.5)
		time.sleep(0)
		pSI=cv.QueryFrame(pCI)
		time.sleep(0)
	
	        cv.PutText(pSI, time.strftime("%d-%m-%y %H:%M:%S", time.gmtime()),pt1, font, cv.RGB(200, 110, 155))
	 
		cv.SaveImage(IMG_PATH+IMG_NAME+".jpg", pSI)
		del pSI
	except:
		del pSI
		image = cv.CreateImage( (200,100), 8, 4)
		cv.PutText(image, "Camera Error",pt1, font, cv.RGB(225, 225, 225))
		cv.SaveImage(IMG_PATH+IMG_NAME+".jpg", image)
		del image

def index(req):
	form = util.FieldStorage(req, keep_blank_values=1)
   	ref = form.getfirst("refresh")
   	forward = form.getfirst("forward")
   	backward = form.getfirst("backward")
	if ref == "Refresh":
		capture()
	if backward == "<":
		RS('b')
		capture()
	if forward == ">":
		RS('f')
		capture()

	req = """
		<html>
		<head></head>
		<body>
		<center>
			<img src='"""+IMG_NAME+""".jpg'/>
			<form action='index.py'>
				<input type='submit' name='backward' value='<'/>
				<input type='submit' name='refresh' value='Refresh'/>
				<input type='submit' name='forward' value='>'/>
			</form>
		</center>
		</body>
		</html>"""
	return req;

