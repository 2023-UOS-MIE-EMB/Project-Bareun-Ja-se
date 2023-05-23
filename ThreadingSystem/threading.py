from multiprocessing import Process, Value, Array,Queue, Manager
import time, os
from cQueue import cQueue
from PacketUtil import cPacketController
import MotorUtils as Motor
import random


#global_motor
gcMotorRequestQ = cQueue() #local Q
gCurrentAngle = Value('i',0) #base value,
gMotorWorking = Value('i',0) #base value,

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
                pMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentAngle, gMotorWorking))
                gcMotorRequestQ = cQueue() #reset
                pMotor.start()

        time.sleep(1)


     
    print( "Main : " , gcMotorRequestQ)

 

 