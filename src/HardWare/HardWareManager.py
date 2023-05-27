import RPi.GPIO as GPIO
import time

def LED(pin : int, time : int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, True)
    time.sleep(time)
    GPIO.output(pin, False) 

    GPIO.cleanup(pin)
