from multiprocessing import Queue
import time
import random

def Detection( alarmTime :int , alarmMode : int , streamingAddr : Queue):
    streamingAddr.cancel_join_thread()
    while(1):
        #todo
        #1.start recognization
        #2.put streaming web ip to streamingAddr 
        print("detecing...")
        #for test
        tmpAddr = str(random.randint(0,4000))

        streamingAddr.put(tmpAddr)
        time.sleep(2)
