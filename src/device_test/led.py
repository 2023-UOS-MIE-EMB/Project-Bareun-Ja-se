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

pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

while(1):
	GPIO.output(pin, True)
	time.sleep(2)
	GPIO.output(pin, False)
