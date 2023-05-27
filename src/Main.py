from multiprocessing import Process, Value, Array,Queue, Manager
import time, os
from myQueue import cQueue
from PacketUtil import cPacketManager
import MotorManager as Motor
import DetectingSleep as Detection
import random

'''
Jeong's Todo List:
-TCP Server
''' 

#global_motor
gpMotor = Process()
gcMotorRequestQ = cQueue()      
gCurrentStage = Value('i',0)                    #base value,

#global_detection
gpDetection = Process()
gStreamingAddr = Queue(1) 
gBaseStreamAddr = "UnvaluableAddr"
#gLatestStreamAddr = ""
gStreamingAddr.put(gBaseStreamAddr)             #base value


if __name__ == '__main__':
    
    #Recv and Send
    while(1): 
        packetManager = cPacketManager()

        sendingContent = { "1" : "10", "2" : "3" }
        result, recvedPacket = packetManager.MakingPacketToSend(sendingContent)

        packetResults = packetManager.ParsingPacket(recvedPacket)

        if( packetResults == None):
            continue  #return to recv

        #Data from (dict)packetResults  
        targetStage = 10
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
        if not ( targetStage == -1) : 
            gcMotorRequestQ.Push(targetStage)
            
            #<Testing>
            for i in range(20):
                #gcMotorRequestQ.Push(i)
                gcMotorRequestQ.Push(random.randint(5,30))
            
            if( gpMotor.is_alive()  == False) : 
                gpMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentStage))
                gcMotorRequestQ.Clean() #reset
                gpMotor.start()

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

            sendingData = {"5" : NowStreamingAddr}

        result , packet = packetManager.MakingPacketToSend(sendingData)

        if(result == False) : 
            print("StreamingError!")
            exit()

        #todo: send Packet
        print(packet)

        time.sleep(1)

    print( "Main : " , gcMotorRequestQ)

 

 