from cQueue import cQueue
from multiprocessing import Value



def CalculatingTime(target : int , current : int ) -> int : 
    resultTime =  current+1
    return resultTime

#@out :   
#currentAngle
def CallingMotor(requestQ : cQueue , currentAngle : Value ):
    while not (requestQ.IsEmpty()):
        item = requestQ.Pop()
        #</Testing
        print( " child : " , item)
        #/>
        time = CalculatingTime(item, currentAngle.value)

        #todo :  
        #   -call motor controller(can not use function, manu controll needed)
        #   -Update currentAngle Value.(can not use function)
        #   내부에서는 임시변수로 current관리하다가 마지막에만 업데이트?
    print("ChildDead")
    return