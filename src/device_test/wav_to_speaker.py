import wave
import RPi.GPIO as GPIO
import time

speaker = 18   # IN과 연결된 GPIO 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(speaker, GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO.PWM(speaker, 1.0)


#wave_read = wave.open("/home/kyj/device_test/watermelonsugar.wav", mode='rb')
wave_read = wave.open("/home/kyj/device_test/8bit.wav", mode='rb')


frame = 0
wave_read.rewind()
wave_read.setpos(44100)
pwm.start(50)

for i in range(0,44100):
        bytes = wave_read.readframes(1)
        freq = (int.from_bytes(bytes, byteorder='big'))
        print(freq)
'''
while True:
    freq = 0
    for i in range(0,44100):
        bytes = wave_read.readframes(1)
        freq = (int.from_bytes(bytes, byteorder='big'))
        print(freq)
    #262,294,330,349,392,440,494,523
    #print(freq)
    #pwm.ChangeFrequency(freq)
    time.sleep(0.5)
    
a = wave_read.getframerate()
b = wave_read.getnchannels()
c = wave_read.getsampwidth()
print('##',a,b,c)

'''
GPIO.cleanup()
