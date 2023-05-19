from multiprocessing import Process, Value, Array,Queue, Manager
import time, os
from myQueue import cQueue
from PacketManager import cPacketManager
import MotorManager as Motor
import DetectingSleep as Detection
from NetWorkManager import cNetWorkManager
import random


gMAXBUF = 512

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

gPacketManager  = cPacketManager()
gNetWorkManager = cNetWorkManager(Hssid="rpi42",maxBuf=512)


'''
@기능 
    자원 회수 기능을 한다.'''
def ReapingResources():

    while(gpMotor.is_alive() ==  False):
        gcMotorRequestQ.Clean() #reset
        gcMotorRequestQ.Push(0) #초기단계로 모터 되돌리기 -> 현재각도값 저장대신 이게 나을지도? 종료될때 최대한 접히는게 보관도 용이할듯
        gpMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentStage))
        gpMotor.start()

    gpMotor.join()

    if( gpDetection.is_alive()  == True ) :
        gpDetection.terminate() 
        time.sleep(2) #neccessary, waiting Process died
     
    gNetWorkManager.__ClientSocket.close()
    gNetWorkManager.__ServerSocket.close()

    return

'''
@기능 
    종료기능을 한다.'''
def ShutingDown():
    ReapingResources()
    os.system("shutdown now")

if __name__ == '__main__':

#Prior-Connect via HotSpot

    # gNetWorkManager.TurnOnHotSpot()
    # gNetWorkManager.SetTCPServerSocket()

    # gNetWorkManager.Listen()
    # gNetWorkManager.Accept()
    # wifiPacket = gNetWorkManager.Recv()
    # WifiDict =  gPacketManager.ParsingPacket(wifiPacket)
    # gNetWorkManager.Close()

    # gNetWorkManager.SetGeneralWiFi(WifiDict["8"],WifiDict["9"])
    # gNetWorkManager.SetTCPServerSocket()
    # gNetWorkManager.Listen()
    # gNetWorkManager.Accept()

    #<\Test>
    gNetWorkManager.SetTCPServerSocket()
    gNetWorkManager.Listen()
    

    #Recv and Send
    while(1): 
        gNetWorkManager.Accept()
        recvedPacket = gNetWorkManager.Recv()

        #for test
        #sendingContent = { "1" : "10", "2" : "3" }
        #result, recvedPacket = packetManager.MakingPacketToSend(sendingContent)

        packetResults = gPacketManager.ParsingPacket(recvedPacket)

        if( packetResults == None):
            continue  #return to recv

        #for test
        #targetStage = 10
        #alarmTime = 5
        #alarmMode = random.randint(0,1)
        #print("Mode is : ", alarmMode)
        #isShutdown = False

        targetStage = int(packetResults["0"])
        alarmTime = int(packetResults["3"])
        alarmMode = int(packetResults["4"])
        isShutdown = int(packetResults["2"])
        
        for key,value in packetResults.items():
            print(key,":", value)

    #power controll
        if(isShutdown):
            ShutingDown()

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
                time.sleep(2) #neccessary, waiting Process died
        
        if( gpDetection.is_alive()  == True ):
            NowStreamingAddr = gStreamingAddr.get()
        else : 
            NowStreamingAddr = gBaseStreamAddr
            
        sendingData = {"5" : NowStreamingAddr}
        result , packet = gPacketManager.MakingPacketToSend(sendingData)

        if(result == False) : 
            print("StreamingError!")
            exit()

        #send Packet
        #gNetWorkManager.SendAll(packet)
        print("senddata: " ,packet)

        time.sleep(1)

 

 