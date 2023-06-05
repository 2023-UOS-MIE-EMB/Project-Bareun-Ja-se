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

    __modeBuzzer = 1 << 0    
    __modeSpeaker = 1 << 1    
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
            GPIO.output(i, False)
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
                print("buzzer")
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
        Speaker & buzzer 를  일정시간 동안  번갈아 가며 울린다.
    @인자
        -time :  전체 동작 시간
        -interval : 각각의 기기가 울리는 시간, speaker와 buzzer 모두 같다.'''
    # def RingBuzzerAndSpeaker(self, times :  int, interval : int) :
    #     self.pwmObj.start(50.0)
    #     if __debug__:
    #         print("both")
    #     for i in range(0, int(times/2*interval) ) :
    #         GPIO.output(self.__buzzer, False)
    #         GPIO.output(self.__speaker,True)
    #         self.pwmObj.ChangeFrequency(200)
    #         time.sleep(interval)
    #         GPIO.output(self.__buzzer, False)
    #         GPIO.output(self.__speaker,True)
    #         self.pwmObj.ChangeFrequency(200)
    #         time.sleep(interval)
            
    #     self.pwmObj.stop()
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
        #elif(alarmMode == self.__modeBoth):
        else:
            print("wrong Mode!")
        
    def resetAll(self):
        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=False)
        self.pwmObj.stop()

if __name__ == "__main__":
    hw = cHardWareManager()

    hw.RingFromMode(2,True)
    time.sleep(3)
    hw.RingFromMode(2,False)
