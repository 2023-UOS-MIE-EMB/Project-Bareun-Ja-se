import RPi.GPIO as GPIO
import time

buzzer = 18   # In과 연결된 GPIO 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO.PWM(buzzer, 1.0)
pwm.start(50.0)

scale = [262,294,330,349,392,440,494,523]

while True:
    for i in range(0,8):
        pwm.ChangeFrequency(scale[i])  # 1이 적당
        time.sleep(1.0)
pwm.stop()
GPIO.cleanup()