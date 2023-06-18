import RPi.GPIO as GPIO
import time

'''
@기능
    led, speaker, buzzer의 gpio제어를 총괄하는 클래스
@생성자 인자 없음'''
class cHardWareManager :
    __outPins = [12,23,24,18]
    __led = 12
    __speaker = 24
    __buzzer =  23
    __pwm = 18

    __modeBuzzer = 1    
    __modeSpeaker =2 
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
        self.resetAll()
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
    '''
    @기능
        Buzzer에게 동작신호
    @인자
        -status 동작신호'''
    def RingSpeaker(self, status :bool) : 

        if (status == True):
            self.pwmObj.start(50.0)
            if __debug__:
                print("speaker")
            GPIO.output(self.__buzzer, False)
            GPIO.output(self.__speaker, True)
            self.pwmObj.ChangeFrequency(200) 

        if (status == False):
            self.pwmObj.stop()
    '''
    @기능
        Buzzer에게 동작신호
    @인자
        -status 동작신호'''
    def RingBuzzer(self, status :bool) : 

        if (status == True):
            self.pwmObj.start(50.0)
            if __debug__:
                print("buzzer")
            GPIO.output(self.__buzzer, True)
            GPIO.output(self.__speaker, False)
            self.pwmObj.ChangeFrequency(1) 

        if (status == False):
            self.pwmObj.stop()
    '''
    @기능
        알람모드에 따라 스피커,부저 를 선택하여 GPIO제어를 통해 제어한다.
    @인자
        - alarmMode : 비트 마스크로 표현된 알람 모드, 제어할 하드웨어를 선택하는데 사용된다. 현재는 1,2 만 존재한다 (1:진동 2: 스피커)
        - action : 하드웨어를 제어할 동작, (True :켜기 False : 끄기)'''
    def RingFromMode(self, alarmMode : int, action : bool) :
        print("alarmMode : ", alarmMode)
        if(alarmMode == self.__modeBuzzer):
            self.RingBuzzer(action)
        elif(alarmMode == self.__modeSpeaker):
            self.RingSpeaker(action)
        else:
            print("wrong Mode!")
    '''
    @기능
        하드웨어 매니저에 등록된 모든 제어기기를 초기 상태로 되돌린다. (끄기)'''
    def resetAll(self):
        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=False)
        self.pwmObj.stop()
#test
if __name__ == "__main__":
    hw = cHardWareManager()

    hw.RingFromMode(2,True)
    time.sleep(3)
    hw.RingFromMode(2,False)
