from cQueue import cQueue
from multiprocessing import Value

'''
@기능
    현재각도와 목표각도를 가지고 모터를 동작할 시간단위를 계산하고 ret하는 함수.
@인자
    -target : 목표 단계
    -current : 현재 단계
@ret 
    -int : 모터를 동작시킬 시간단위 수'''
def CalculatingTime(target : int , current : int ) -> int : 
    resultTime =  current+1
    return resultTime

'''
@기능
    모터동작을 수행하는 함수.  목표 단계 가 담긴 requestQ가 비워질 때 까지 요청을 하나씩 처리한다. 
@인자
    -requestQ  :  목표 단계 요청이 담긴 Queue, 공유 메모리 공간으로서의 Queue가 아니다.
    
@OUT
    -currentStage : 모터의 현재단계. 다른 프로세스와 공유가능한 값이다. 요청 처리 후 바뀐다.'''
def CallingMotor(requestQ : cQueue , currentStage : Value ):
    while not (requestQ.IsEmpty()):
        item = requestQ.Pop()
        #</Testing
        print( " child : " , item)
        #/>
        time = CalculatingTime(item, currentStage.value)

        #todo :  
        #   -call motor controller(can not use function, manu controll needed)
        #   -Update currentAngle Value.(can not use function)
        #   내부에서는 임시변수로 current관리하다가 마지막에만 업데이트?
    print("ChildDead")
    return