import RPi.GPIO as GPIO
import time

speaker = 18   # IN과 연결된 GPIO 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(speaker, GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO.PWM(speaker, 1.0)
pwm.start(70.0)

while True:
    pwm.ChangeFrequency(200)  # 

pwm.stop()
GPIO.cleanup()



