import RPi.GPIO as GPIO
import time

def led(pin, t):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, True)
    time.sleep(t)
    GPIO.output(pin, False) 

    GPIO.cleanup(pin)

#led(17, 5)  

pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.setwarnings(False)

while(1):
    GPIO.output(pin, True)
    time.sleep(1)
    GPIO.output(pin, False)
    time.sleep(1)

