from multiprocessing import Process, Value, Array,Queue, Manager
import time
import cQueue

def pushing(q, item):
    
    while(1):
        q.Push(item)
        time.sleep(1)

def Poping(q : cQueue):
    while(1):
        while not (q.Empty()):
            print(q.Pop())
        time.sleep(5)

if __name__ == '__main__':

    q = cQueue()
  
    p1 = Process(target=pushing, args=( q, 1))
    p2 = Process(target=Poping, args=( q,))
    p1.start()
    p2.start()

    time.sleep(10)

    p1.terminate()
    p2.terminate()
 