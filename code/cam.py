import cv2
import time
import os
#from matplotlib import pyplot as plt

cam = cv2.VideoCapture("/dev/video0")
ret, frame = cam.read()
cv2.imwrite('/home/rpi4/code/entry_photo/licence_plate.jpg',frame)
cv2.imwrite('/home/rpi4/tmp/licence_plate.jpg',frame)
cam.release()
os.system("sshpass -p 'raspberry' scp /home/rpi4/code/entry_photo/licence_plate.jpg pi@192.168.217.101:/home/pi/entry_photo")
exit(0)