from cQueue import cQueue
from multiprocessing import Value



def CalculatingTime(target : int , current : int ) -> int : 
    resultTime =  current+1
    return resultTime

#out :  currentAngle
def CallingMotor(requestQ : cQueue , currentAngle : Value , isWorking : Value):
    isWorking =  True
    while not (requestQ.IsEmpty()):
        item = requestQ.Pop()
        #</Testing
        print( " child : " , item)
        #/>
        time = CalculatingTime(item, currentAngle.value)

        #todo :  
        #   -call motor controller(can not use function)
        #   -Update current Value.(can not use function)
    isWorking = False
    print("ChildDead")
    return