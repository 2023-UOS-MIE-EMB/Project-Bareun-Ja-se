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
gCurrentAngle = Value('i',0)                    #base value,

#global_detection
gpDetection = Process()
gStreamingAddr = Queue(1) 
gBaseStreamAddr = "UnvaluableAddr"
#gLatestStreamAddr = ""
gStreamingAddr.put(gBaseStreamAddr)             #base value


if __name__ == '__main__':
    
    #Recv and Send
    while(1): 
        recvedPacket = "recved msg from client"
        packetManager = cPacketController()
   
        if(packetManager.ParsingPacket(recvedPacket) == False):
            continue  #return to recv

        packetResults = packetManager.GetBody()

        #Data from (dict)packetResults  
        targetAngle = 10
        alarmTime = 5
        alarmMode = random.randint(0,1)
        print("Mode is : ", alarmMode)
        isShutdown = False

    #power controll
        if(isShutdown):
            #todo:
            #   -set device initial pose via motor
            #   -resources reaping 
            #   os("shutdown now")
            exit()

    #motor
        #if not ( targetAngle == -1) : 
        #    gcMotorRequestQ.Push(targetAngle)
            
        #    #</Testing
        #    for i in range(20):
        #        gcMotorRequestQ.Push(i)
        #       #gcMotorRequestQ.Push(random.randint(5,30))
        #    #/>
        #    if( gpMotor.is_alive()  == False) : 
        #        gpMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentAngle))
        #        gcMotorRequestQ = cQueue() #reset
        #        gpMotor.start()

    #detectomg sleep
        if not (alarmMode == 0) :  #need detection
            if(gpDetection.is_alive()  == False ) : #but detection doesn't work, turn on detection process
                gpDetection = Process(target=Detection.Detection, args=(alarmTime, alarmMode, gStreamingAddr))
                gpDetection.start()

        else :
            if( gpDetection.is_alive()  == True ) : #but detection is working now, turn off detection process
                gpDetection.terminate() 
                time.sleep(1) #neccessary, waiting Process died
        
        if( gpDetection.is_alive()  == True ):
            NowStreamingAddr = gStreamingAddr.get()
        else : 
            NowStreamingAddr = gBaseStreamAddr

        result , packet = packetManager.MakingPacketToSendClient(NowStreamingAddr)

        if(result == False) : 
            print("StreamingError!")
            exit()

        #todo: send Packet
        print(packet)

        time.sleep(1)


     
    print( "Main : " , gcMotorRequestQ)

 

 