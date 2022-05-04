import cv2
from defer import return_value
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
import threading
import sys
import pymysql
from datetime import datetime

##take photo
os.system("python3 /home/rpi4/code/cam.py")
#print("complete take photo")


##detect licence plate./darknet detector test data/licence_plate.data cfg/yolov4-tiny-licence_plate.cfg yolov4-tiny-licence_plate_final.weights -ext_output /home/rpi4/code/entry_photo/licence_plate.jpg | grep left: >> /home/rpi4/code/coordinate.txt
os.system("cd /home/rpi4/yolov4/darknet/ && ./darknet detector test data/licence_plate.data cfg/yolov4-tiny-licence_plate.cfg yolov4-tiny-licence_plate_final.weights -ext_output /home/rpi4/code/entry_photo/licence_plate.jpg | grep left > /home/rpi4/code/coordinate.txt")


##get detect result coordinate & cut photo
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


##OCR
reader = easyocr.Reader(['en']) # need to run only once to load model into memory
result = reader.readtext('/home/rpi4/code/tmp/tmp.jpg', detail = 0)
result2 = "".join(result)
result3 = re.sub(r'[^\w\s]','',result2)
print(result3) 



##send to database
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
    
def insertBLOB_toMySQL(numplate,picture):

   print("Inserting BLOB into NUMPIC_DATA table")
   try:
      db = pymysql.connect(host='192.168.217.100',user='parking',password='!QAZ2wsx',database='TESTDB') #test.py與MySQL連線
   
      mycursor = db.cursor()
   
      #sql2= "UPDATE NUMPIC_DATA SET picture=LOAD_FILE('C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg') where numplate=%s" %(ocr_result)
      sql2= "INSERT INTO NUMPIC_DATA(numplate,picture) VALUES(%s,%s)"
   
      empPicture = convertToBinaryData(picture)
   
      # Convert data into tuple format
      insert_blob_tuple = (numplate,empPicture)
      mycursor.execute(sql2, insert_blob_tuple)
      db.commit()
      print("Image inserted successfully as a LONGBLOB into NUMPIC_DATA table")

   except pymysql.connect.Error as error:
      print(f"Failed inserting BLOB data into NUMPIC_DATA table:\n {error}")

def write_file(data,filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB_fromMySQL(picture):
    print("Reading BLOB data from NUMPIC_DATA table \n")

    try:
        db = pymysql.connect(host='192.168.217.100',user='parking',password='!QAZ2wsx',database='TESTDB') #test.py與MySQL連線

        mycursor = db.cursor()

        mycursor.execute("SELECT picture from NUMPIC_DATA")
        all_data = mycursor.fetchall()
        for row in all_data:
            image = row[0]
            write_file(image, picture)
        print("Storing picture and bio-data on 'C:\MCUT_file\Independent Study\MySQL\Picture\Stored_pic\' \n")
        print("Success!")

    except pymysql.connect.Error as error:
        print(f"Failed read BLOB data from NUMPIC_DATA table:\n {error}")



# Prepare SQL query to INSERT a record into the database.

now = datetime.now()
ct=now.strftime("%Y-%m-%d_%H%M%S")
print("current time:",ct)

# Open database connection
db = pymysql.connect(host='192.168.217.100',user='parking',password='!QAZ2wsx',database='TESTDB')

# prepare a cursor object using cursor() method
mycursor = db.cursor()

try:

   #ocr_result='NAF-7393'

   # Execute the SQL command

   #mycursor.execute("INSERT INTO NUMPIC_DATA(numplate) VALUES('%s')" % (ocr_result))

   #insertBLOB_toMySQL(ocr_result,"C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg")
   insertBLOB_toMySQL(result3,"/home/rpi4/code/entry_photo/licence_plate.jpg")
   #filename=f'{ct}.jpg'
   #readBLOB_fromMySQL(f"C:\MCUT_file\Independent Study\MySQL\Picture\Stored_pic\{filename}")
   
   mycursor.execute("UPDATE NUMPIC_DATA SET in_time='%s', payment_status='%s', payment=null, payment_time=null, out_time=null, \
      extra_payment=null where numplate='%s'" % (ct, 'undone', result3))
   
   # Commit your changes in the database
   db.commit()
   print("All Data inserted")
except:
   # Rollback in case there is any error
   db.rollback()


# disconnect from server
db.close()


##open & close fence 
CONTROL_PIN = 12
PWM_FREQ = 50
STEP=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.27 * PWM_FREQ * angle / 180)
    return duty_cycle

def switch2deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

degrees = [50,0]

for i in range(1):
    for deg in degrees:
        switch2deg(deg)
        time.sleep(0.5)

pwm.stop()
GPIO.cleanup()

##send ocr result to HDMI
app = Tk()
app.title("入場")
app_scale = Canvas(height=150, width=600)
lbl1 = Label(app, text="歡迎光臨",font=('Arial', 25))
lbl1.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
lbl2 = Label(app, text = result3,font=('Arial', 30))#製作一個label並顯示車牌號碼和控制字體、大小
lbl2.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
#\抓取系統時間\
localtime = time.localtime()
timeresult = time.strftime("%Y-%m-%d %H:%M:%S %p", localtime)
lbl3 = Label(app, text=timeresult,font=('Arial', 20))
lbl3.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.N+tk.E)
#app_scale.grid()
def close():
    time.sleep(10)
    app.destroy()

stop_threads = False
t=threading.Thread(target=close)
t.start()
app.mainloop()
os.system("sudo python3 /home/rpi4/code/close_fence.py")
stop_threads = True


os.system("rm -rf /home/rpi4/code/entry_photo/*")
os.system("rm -rf /home/rpi4/code/tmp/*")
os._exit(0)

