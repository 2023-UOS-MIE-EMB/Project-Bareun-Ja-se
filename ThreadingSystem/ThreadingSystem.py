#https://docs.python.org/2/library/multiprocessing.html#pipes-and-queues   << docs for multiprocessing

from glob import glob
from multiprocessing import Process, shared_memory, Queue, Value, Pool, TimeoutError, Lock
import ForTesting as test
import time
import socket



#global shared_memory
gCurrentAngle = Value('d',0.0)  

'''
@기능
    요청Q가 빌때까지 Q값을 받아 모터를 동작시키는 함수. 
@변수
    requestQ : 목표각도 값이 들어있는 queue이다. Empty에대한 동작이 불완전할 수 있다. (라이브러리 한계)
@리턴
'''
def ControllingMotor(requestQ : Queue):
    global gCurrentAngle

    time.sleep(0.2)
    while( requestQ.empty() != True ) :   
        target = requestQ.get()
        time = CalculatingMotorTime(gCurrentAngle, target)
        if(test.ControllingMotorWithTime(time) != True) :
            return
        time.sleep(0.2)
    return
'''
@기능
    모터의 현재각도를 토대로 모터 동작시간을 계산하는 함수
@변수
    currentAngle : 모터의 현재 각도
    targerAngle : 모터의 목표 각도
@리턴
    int : 모터 동작시간, 양수면 시계방향, 음수면 반시계방향이다.
'''
def CalculatingMotorTime(currentAngle : int , targetAngle : int) -> int : 
    return (currentAngle+1) %45

if __name__ == "__main__" : 
    cgAngleRequestQ = Queue()

