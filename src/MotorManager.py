from myQueue import cQueue
from multiprocessing import Value
import RPi.GPIO as GPIO

'''
@기능
    모터 하드웨어 제어를 총괄하는 클래스
@생성자
    - rpmSleep -> rpm을 조절하는 수, 실제 rpm이 아닌, 동작 사이의 sleep시간이다.
    - cycle -> 모터 드라이버에 따른 1step에 해당하는 회전수
@주의사항
    현시스템에서는 모터제어 프로세스만 호출한다. 외부에서 사용하지 말것.'''
class __cMotorManager() :

    __outPins = [21,13,19,24]
    __power = 21  #3.3V out
    __ena = 13
    __dir = 19
    __clk = 24

    __rpmSleep = 0.005
    __cycle = 6400

    def __int__(rpmSleep:float = 0.005 , cycle:int = 6400):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings (False)
        
        __rpmSleep = rpmSleep
        __cycle = cycle

        for i in self.__outPins:
            GPIO.setup(i, GPIO.OUT,initial=True)

    def __del__(self):
        for i in self.__outPins:
            GPIO.cleanup(i)
        return

    def RotatingMotor(cycles : int):   
         
        if( cycles < 0 ) :
            GPIO.output(__dir, False)  #CCW
            cycles =  -cycles
        else : 
            GPIO.output(__dir, True)  #CW

        for i in range(cycles):
            GPIO.output(__clk, True)   
            time.sleep(__rpmSleep)
            GPIO.output(__clk, False)    
            time.sleep(__rpmSleep)

'''
@기능
    현재 단계와 목표 단계를 가지고 모터를 동작할 시간단위를 계산하고 ret하는 함수.
@인자
    -target : 목표 단계
    -current : 현재 단계
@ret 
    -int : 모터를 동작시킬 사이클수'''
def CalculatingTime(target : int , current : int ) -> int : 
    resultTime =  (current+1) % 300
    return resultTime

'''
@기능
    모터동작을 수행하는 함수.  목표 단계 가 담긴 requestQ가 비워질 때 까지 요청을 하나씩 처리한다. 
@인자
    -requestQ  :  목표 단계 요청이 담긴 Queue, 공유 메모리 공간으로서의 Queue가 아니다.
    
@OUT
    -currentStage : 모터의 현재단계. 다른 프로세스와 공유가능한 값이다. 요청 처리 후 바뀐다.'''
def CallingMotor(requestQ : cQueue , currentStage : Value ):

    motor = __cMotorManager()

    while not (requestQ.IsEmpty()):
        nowTarget = requestQ.Pop()
        tmpCurrentStage = currentStage.value
        #</Testing
        print( " child : " , nowTarget)
        #/>
        cycles = CalculatingTime(nowTarget, tmpCurrentStage)

        motor.RotatingMotor(cycles)
        tmpCurrentStage = nowTarget

    currentStage =  tmpCurrentStage #save
    print("ChildDead")
    return