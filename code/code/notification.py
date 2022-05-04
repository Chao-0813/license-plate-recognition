import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#set GPIO
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
#turn on LED
GPIO.output(4, GPIO.LOW)
GPIO.output(5, GPIO.LOW) 
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW) 