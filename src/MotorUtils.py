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
        #   ���ο����� �ӽú����� current�����ϴٰ� ���������� ������Ʈ?
    print("ChildDead")
    return