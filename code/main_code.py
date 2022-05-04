import RPi.GPIO as GPIO
import os

#set GPIO
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

#initial LED
os.system("python3 LED_initial.py")

#detect switch status
while True: # Run forever
    if GPIO.input(19) == GPIO.HIGH:
        os.system("python3 entry2.py")
        GPIO.output(4,GPIO.HIGH)
        GPIO.output(5,GPIO.LOW)
        GPIO.output(22,GPIO.HIGH)
        GPIO.output(27,GPIO.LOW)
        print("entry end")

    elif GPIO.input(16) == GPIO.HIGH:
        #os.system("python3 exit.py")
        GPIO.output(4,GPIO.LOW)
        GPIO.output(5,GPIO.HIGH)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(27,GPIO.HIGH)
        print("exit")

    elif GPIO.input(19) == GPIO.LOW & GPIO.input(16) == GPIO.LOW:
        GPIO.output(4,GPIO.LOW)
        GPIO.output(5,GPIO.LOW)
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(22,GPIO.HIGH)
       
        
        

