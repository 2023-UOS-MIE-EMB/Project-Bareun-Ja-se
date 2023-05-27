import RPi.GPIO as GPIO
import time

dir = [5,26]   # -,+
ena = [6,13]    # -,+
clk = [20,17]   # -.+

GPIO.setmode(GPIO.BCM)

for p in clk:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, True)

for p in ena:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, True)

for p in dir:
    GPIO.setup(p, GPIO.OUT)

#cw
GPIO.output(5, 1)
GPIO.output(26, 1)

while(1):
    for p in clk:
        GPIO.output(20, True)
    time.sleep(0.0001)
    for p in clk:
        GPIO.output(20, False)
    time.sleep(0.0001)
