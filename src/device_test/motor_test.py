import RPi.GPIO as GPIO
import time

pin = [20, 17, 6, 13]
direc = [26, 19]

#(CCW)
seq2 = [
       [1, 0, 0, 1],
       [1, 0, 1, 0],
       [0, 1, 0, 1],
       [0, 1, 1, 0]]
#19(CW)
seq = [
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 1, 0]]


seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]]

GPIO.setmode(GPIO.BCM)

for p in pin:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, False)

for p in direc:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, False)


stepcnt = 0
GPIO.output(26, True)

while (1):
    for p in range(0,4):
	    xpin = pin[p]
	    if seq[stepcnt][p] == 0:
	        GPIO.output(xpin,True)
	    else:
	        GPIO.output(xpin,False)
    stepcnt += 1
    stepcnt = stepcnt%8
    time.sleep(0.001)
    
GPIO.cleanup()