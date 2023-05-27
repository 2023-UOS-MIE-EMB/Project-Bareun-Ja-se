import RPi.GPIO as GPIO
import time
    

#1.5A / 1/16    
GPIO.setmode(GPIO.BCM)

dir = 27
ena = 22
clk = 17

plus = [16,20,21]

for i in plus:
    GPIO.setup(i, GPIO.OUT, initial=True)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(dir, GPIO.OUT,initial=True)
GPIO.setup(ena, GPIO.OUT,initial=True)
GPIO.setup(clk, GPIO.OUT,initial=True)

while(1):
    GPIO.output(dir, True)
    print(GPIO.input(dir))
    for i in range(3000):
        GPIO.output(clk, True)   
        time.sleep(0.001)
        GPIO.output(clk, False)    
        time.sleep(0.001)
    GPIO.output(dir,False )
    print(GPIO.input(dir))
    for i in range(3000):
        GPIO.output(clk,True)
        time.sleep(0.001)
        GPIO.output(clk, False)    
        time.sleep(0.001)
         