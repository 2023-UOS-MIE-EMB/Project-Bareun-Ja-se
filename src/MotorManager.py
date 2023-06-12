from myQueue import cQueue
from multiprocessing import Value
import RPi.GPIO as GPIO
import time

'''
@기능
    모터 하드웨어 제어를 총괄하는 클래스
@생성자
    - rpmSleep -> rpm을 조절하는 수, 실제 rpm이 아닌, 동작 사이의 sleep시간이다.
    - cycle -> 모터 드라이버에 따른 1step에 해당하는 회전수
@주의사항
    현시스템에서는 모터제어 프로세스만 호출한다. 외부에서 사용하지 말것.'''
class __cMotorManager() :

    __outPins = [21,13,19,26]
    __power = 21  #3.3V out
    __ena = 13
    __dir = 19
    __clk = 26

    __rpmSleep = 0.005
    __cycle = 6400

    def __init__(self,rpmSleep:float = 0.005 , cycle:int = 6400):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings (False)
        
        self.__rpmSleep = rpmSleep
        self.__cycle = cycle

        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=True)

    def __del__(self):
        for i in self.__outPins:
            GPIO.cleanup(i)
        return

    def RotatingMotor(self, cycles : int): 
        print("rotating:",cycles)  
        if( cycles < 0 ) :
            GPIO.output(self.__dir, False)  #CCW
            cycles =  -cycles
        else : 
            GPIO.output(self.__dir, True)  #CW

        cycles = cycles * 100

        for i in range(cycles):
            GPIO.output(self.__clk, True)   
            time.sleep(self.__rpmSleep)
            GPIO.output(self.__clk, False)    
            time.sleep(self.__rpmSleep)

'''
@기능
    현재 단계와 목표 단계를 가지고 모터를 동작할 시간단위를 계산하고 ret하는 함수.
@인자
    -target : 목표 단계
    -current : 현재 단계
@ret 
    -int : 모터를 동작시킬 사이클수'''
def CalculatingTime(target : int , current : int ) -> int : 
    result =  (target - current)
    return result

'''
@기능
    모터동작을 수행하는 함수.  목표 단계 가 담긴 requestQ가 비워질 때 까지 요청을 하나씩 처리한다. 
@인자
    -requestQ  :  목표 단계 요청이 담긴 Queue, 공유 메모리 공간으로서의 Queue가 아니다.
    
@OUT
    -currentStage : 모터의 현재단계. 다른 프로세스와 공유가능한 값이다. 요청 처리 후 바뀐다.'''
def CallingMotor(requestQ : cQueue , currentStage : Value ):

    minStage = 1
    maxStage =20 

    motor = __cMotorManager()
    tmpCurrentStage = currentStage.value
    print("child")
    if __debug__ :
        requestQ.PrintAll()
    while not (requestQ.IsEmpty()):
        nowTarget = requestQ.Pop()
        if(nowTarget < minStage ): 
            continue
        nowTarget = min(nowTarget,maxStage) 
        
        #</Testing
        if __debug__ :
            requestQ.PrintAll()
            print( " child : " , nowTarget)
        #/>
        cycles = CalculatingTime(nowTarget, tmpCurrentStage)

        motor.RotatingMotor(cycles)
        tmpCurrentStage = nowTarget
    del(motor)
    currentStage.value =  tmpCurrentStage #save
    print("ChildDead, CurrentStage :", currentStage.value)
    return

if __name__ == '__main__':
    mm = __cMotorManager()
    mm.RotatingMotor(1000)
    mm.RotatingMotor(-1000)
