import RPi.GPIO as GPIO
import time

'''
@���
    led, speaker, buzzer�� gpio��� �Ѱ��ϴ� Ŭ����
@������ ���� ����'''
class cHardWareManager :
    __outPins = [12,23,24,18]
    __led = 12
    __speaker = 23
    __buzzer =  24
    __pwm = 18

    pwmObj = None

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings (False)

        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=False)

        self.pwmObj = GPIO.PWM(__pwm,1.0)
        
        return

    def __del__(self):
        for i in self.__outPins:
            GPIO.cleanup(i)
        return
    '''
    @���
        LED�� ���� ��ȣ�� ������.
    @����
        -action :  True -> on, False ->off'''
    def RingLED(self, action :  bool):
        GPIO.output(self.__led, action)
        time.sleep(time)
    '''
    @���
        Buzzer�� �����ð� ���� �︰��.
    @����
        -time :  Buzzer�� �︱ �ð�'''
    def RingBuzzer(self, time :  int) : 
        self.pwmObj.start(50.0)

        GPIO.output(self.__buzzer, True)
        GPIO.output(self.__speaker, False)
        self.pwmObj.ChangeFrequency(1) 
        time.sleep(time)

        self.pwmObj.stop()
    '''
    @���
        Speaker�� �����ð� ���� �︰��.
    @����
        -time :  speaker�� �︱ �ð�'''
    def RingSpeaker(self, time :  int) : 
        self.pwmObj.start(50.0)

        GPIO.output(self.__buzzer, False)
        GPIO.output(self.__speaker,True)
        self.pwmObj.ChangeFrequency(200)
        time.sleep(time)

        self.pwmObj.stop()
    '''
    @���
        Speaker & buzzer ��  �����ð� ����  ������ ���� �︰��.
    @����
        -time :  ��ü ���� �ð�
        -interval : ������ ��Ⱑ �︮�� �ð�, speaker�� buzzer ��� ����.'''
    def RingBuzzerAndSpeaker(self, time :  int, interval : int) :
        self.pwmObj.start(50.0)

        for i in range(0, int(time/2*interval) ) :
            GPIO.output(self.__buzzer, False)
            GPIO.output(self.__speaker,True)
            self.pwmObj.ChangeFrequency(200)
            time.sleep(interval)
            GPIO.output(self.__buzzer, False)
            GPIO.output(self.__speaker,True)
            self.pwmObj.ChangeFrequency(200)
            time.sleep(interval)
            
        self.pwmObj.stop()




