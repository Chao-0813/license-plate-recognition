import cv2
import numpy as np
import re
import os
import easyocr
import tkinter as tk 
import time
from tkinter import *
from numpy import array
from cv2 import line
import RPi.GPIO as GPIO

#take photo
os.system("python3 /home/rpi4/code/cam.py")
#print("complete take photo")


#detect licence plate./darknet detector test data/licence_plate.data cfg/yolov4-tiny-licence_plate.cfg yolov4-tiny-licence_plate_final.weights -ext_output /home/rpi4/code/entry_photo/licence_plate.jpg | grep left: >> /home/rpi4/code/coordinate.txt
os.system("cd /home/rpi4/yolov4/darknet/ && ./darknet detector test data/licence_plate.data cfg/yolov4-tiny-licence_plate.cfg yolov4-tiny-licence_plate_final.weights -ext_output /home/rpi4/code/entry_photo/licence_plate.jpg | grep left > /home/rpi4/code/coordinate.txt")


#get detect result coordinate
coor=[] #yolov4 coordinate
with open('/home/rpi4/code/coordinate.txt') as f:
    tmp=f.read()
coor = [int(s) for s in re.findall(r'-?\d+\.?\d*', tmp)]
y1 = coor[2]
y2 = coor[2] + coor[4]
x1 = coor[1]
x2 = coor[1] + coor[3]
img = cv2.imread('/home/rpi4/yolov4/darknet/predictions.jpg')
cropped = img[y1:y2,x1:x2] #img[y:y+h, x:x+w]
gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY) #**使相片灰階化命名為gray** 
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) #**二值化**
cv2.imwrite('/home/rpi4/code/tmp/tmp.jpg',binary)


#OCR
reader = easyocr.Reader(['en']) # need to run only once to load model into memory
result = reader.readtext('/home/rpi4/code/tmp/tmp.jpg', detail = 0)
print(result) 
