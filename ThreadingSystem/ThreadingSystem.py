#https://docs.python.org/2/library/multiprocessing.html#pipes-and-queues   << docs for multiprocessing

from glob import glob
from multiprocessing import Process, shared_memory, Queue, Value, Pool, TimeoutError, Lock
import ForTesting as test
import time
import socket



#global shared_memory
gCurrentAngle = Value('d',0.0)  

'''
@���
    ��ûQ�� �������� Q���� �޾� ���͸� ���۽�Ű�� �Լ�. 
@����
    requestQ : ��ǥ���� ���� ����ִ� queue�̴�. Empty������ ������ �ҿ����� �� �ִ�. (���̺귯�� �Ѱ�)
@����
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
@���
    ������ ���簢���� ���� ���� ���۽ð��� ����ϴ� �Լ�
@����
    currentAngle : ������ ���� ����
    targerAngle : ������ ��ǥ ����
@����
    int : ���� ���۽ð�, ����� �ð����, ������ �ݽð�����̴�.
'''
def CalculatingMotorTime(currentAngle : int , targetAngle : int) -> int : 
    return (currentAngle+1) %45

if __name__ == "__main__" : 
    cgAngleRequestQ = Queue()

