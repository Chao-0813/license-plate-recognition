import time
import RPi.GPIO as GPIO
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

degrees = [0,50]

for i in range(1):
    for deg in degrees:
        switch2deg(deg)
        time.sleep(0.5)

pwm.stop()
GPIO.cleanup()

exit(0)
