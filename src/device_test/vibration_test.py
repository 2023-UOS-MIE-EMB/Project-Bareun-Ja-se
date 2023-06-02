import RPi.GPIO as GPIO
import time

vccs = [24, 27]
pwm = 18   # In과 연결된 GPIO 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm, GPIO.OUT,initial=False)
for i in vccs:
    GPIO.setup(i, GPIO.OUT,initial=False)
    
GPIO.setwarnings(False)

pwm = GPIO.PWM(pwm, 1.0)
pwm.start(50.0)


# GPIO.output(vccs[0],True) #buzz
# GPIO.output(vccs[1],False) #speaker
# pwm.ChangeFrequency(1)  # 1이 적당

# time.sleep(3)
for i in range(10):
    for i in range(0,3):
        GPIO.output(vccs[0],False) #buzz
        GPIO.output(vccs[1],True) #speaker
        pwm.ChangeFrequency(200)  # 1이 적당
        time.sleep(1)

    for i in range(0,3):
        GPIO.output(vccs[0],True) #speaker
        GPIO.output(vccs[1],False) #speaker
        pwm.ChangeFrequency(1)  # 1이 적당
        time.sleep(1)

pwm.stop()
GPIO.cleanup()








