import RPi.GPIO as GPIO
import time

'''
@기능
    led, speaker, buzzer의 gpio제어를 총괄하는 클래스
@생성자 인자 없음'''
class cHardWareManager :
    __outPins = [12,23,24,18]
    __led = 12
    __speaker = 23
    __buzzer =  24
    __pwm = 18

    __modeBuzzer = 0 << 1    
    __modeSpeaker = 0 << 2    
    __modeBoth = __modeBuzzer | __modeSpeaker  

    pwmObj = None

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings (False)

        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=False)

        self.pwmObj = GPIO.PWM(self.__pwm,1.0)
        
        return

    def __del__(self):
        for i in self.__outPins:
            GPIO.cleanup(i)
        return
    '''
    @기능
        LED에 동작 신호를 보낸다.
    @인자
        -action :  True -> on, False ->off'''
    def RingLED(self, action :  bool):
        GPIO.output(self.__led, action)
        time.sleep(time)
    '''
    @기능
        Buzzer를 일정시간 동안 울린다.
    @인자
        -time :  Buzzer를 울릴 시간'''
    def RingBuzzer(self, time :  int) : 
        self.pwmObj.start(50.0)

        GPIO.output(self.__buzzer, True)
        GPIO.output(self.__speaker, False)
        self.pwmObj.ChangeFrequency(1) 
        time.sleep(time)

        self.pwmObj.stop()
    '''
    @기능
        Speaker를 일정시간 동안 울린다.
    @인자
        -time :  speaker를 울릴 시간'''
    def RingSpeaker(self, time :  int) : 
        self.pwmObj.start(50.0)

        GPIO.output(self.__buzzer, False)
        GPIO.output(self.__speaker,True)
        self.pwmObj.ChangeFrequency(200)
        time.sleep(time)

        self.pwmObj.stop()
    '''
    @기능
        Speaker & buzzer 를  일정시간 동안  번갈아 가며 울린다.
    @인자
        -time :  전체 동작 시간
        -interval : 각각의 기기가 울리는 시간, speaker와 buzzer 모두 같다.'''
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
    '''
    @기능
        bitmask AlarmMode에 따라 스피커와 부저 제어
    @인자
        -alarmMode : 비트마스킹 알람 모드, ([스피커][부저])
        -workingTime : 알람이 울리는 시간 '''
    def RingFromMode(self, alarmMode : int, workingTime : int) :

        if(alarmMode == self.__modeBuzzer):
            self.RingBuzzer(workingTime)
        elif(alarmMode == self.__modeSpeaker):
            self.RingSpeaker(workingTime)
        elif(alarmMode == self.__modeBoth):
            self.RingBuzzerAndSpeaker(workingTime,workingTime/2)
        else:
            print("wrong Mode!")





