from multiprocessing import Process, Value, Array,Queue, Manager
import time, os
from cQueue import cQueue
from PacketUtil import cPacketController
import MotorUtils as Motor
import DetectingSleep as Detection
import random


#global_motor
gpMotor = Process()
gcMotorRequestQ = cQueue()      
gCurrentAngle = Value('i',0)    #base value,
gMotorWorking = Value('i',0)    #base value,

#global_detection
gpDetection = Process()
gDetectionWorking = Value('i',0)    #base value,
gStreamingAddr = Queue(1)           
gStreamingAddr.put("https://127.0.0.1:5000")          #base value


if __name__ == '__main__':
    


    #ecv and Send
    while(1): 
        recvedPacket = "recved msg from client"
        packetManager = cPacketController()
   
        if(packetManager.ParsingPacket(recvedPacket) == False):
            exit()

        packetResults = packetManager.GetBody()

        #(dict)packetResults ���� �̾Ƴ� �����ȣ��� ����.
        targetAngle = 10
        isStreaming = False
        alarmTime = 5
        alarmMode = 0 << 1 
        isShutdown = False

    #power controll
        if(isShutdown):
            #todo:
            #   -set device initial pose via motor
            #   -resources reaping 
            #   os("shutdown now")
            exit()

    #motor

        if not ( targetAngle == -1) : 
            gcMotorRequestQ.Push(targetAngle)
            
            #</Testing
            for i in range(20):
                gcMotorRequestQ.Push(i)
               #gcMotorRequestQ.Push(random.randint(5,30))
            #/>
            if( bool(gMotorWorking.value)  == False) : 
                gpMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentAngle, gMotorWorking))
                gcMotorRequestQ = cQueue() #reset
                gpMotor.start()

    #detectomg sleep
        
        if not (alarmMode == 0) :  #need detection
            if( gDetectionWorking.value  == False ) : #but detection doesn't work, turn on detection process
                pDetection = Process(target=Detection.Detection(), args=(alarmTime, alarmMode, gStreamingAddr))

        else :
            if( gDetectionWorking.value  == True ) : #but detection is working now, turn off detection process
                print(1)

        

    #streaming



        time.sleep(1)


     
    print( "Main : " , gcMotorRequestQ)

 

 