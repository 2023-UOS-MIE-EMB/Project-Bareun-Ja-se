from multiprocessing import Process, Value, Array,Queue, Manager
import time, os
from myQueue import cQueue
from PacketManager import cPacketManager
import MotorManager as Motor
#import DetectingSleep as Detection
from NetWorkManager import cNetWorkManager
import random


from facedetect_module import cFaceDetector
import socket
from flask import Flask, Response
import utils


gMAXBUF = 512

#global_motor
gpMotor = Process()
gcMotorRequestQ = cQueue()      
gCurrentStage = Value('i',1)                    #base value,

#global_detection
gpApp : Flask = Flask(__name__)
gFace_detector : cFaceDetector = None
gpDetection = Process()
gBaseStreamAddr = "UnvaluableAddr"
gStreamingAddr = gBaseStreamAddr

@gpApp.route('/vid')
def vid():
    global gFace_detector
    return Response(gFace_detector.detecting_face_for_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')

#global_networking
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
        print("kill")
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

    gNetWorkManager.SetTCPServerSocket()
    gNetWorkManager.Listen()
    
    while(1): 
        
        gNetWorkManager.Accept()
        recvedPacket = gNetWorkManager.Recv()

        packetResults = gPacketManager.ParsingPacket(recvedPacket)

        if( packetResults == None):
            continue  #return to recv

        targetStage = int(packetResults["0"])
        strmRequest = int(packetResults["1"])
        print(strmRequest)
        alarmTime = int(packetResults["3"]) * 60  #min to sec
        alarmMode = int(packetResults["4"])
        isShutdown = int(packetResults["2"])
        
        for key,value in packetResults.items():
            print(key,":", value)

    # #power controll
    #     if(isShutdown):
    #         ShutingDown()

    #motor
        if not ( targetStage == -1) : 
            gcMotorRequestQ.Push(targetStage)
            print("nowQ: ")
            gcMotorRequestQ.PrintAll()
            
            #<Testing>
            # for i in range(20):
            #     #gcMotorRequestQ.Push(i)
            #     gcMotorRequestQ.Push(random.randint(5,30))
            
            if( gpMotor.is_alive()  == False) : 
                gpMotor = Process(target=Motor.CallingMotor, args=( gcMotorRequestQ,gCurrentStage))
                gpMotor.start()
                gcMotorRequestQ.Clean() #reset
                
    #strmRequest
        if( strmRequest == True):
            if( gpDetection.is_alive()  == True ) : #but detection is working now, turn off detection process
                    gpDetection.terminate() 
                    time.sleep(2) #neccessary, waiting Process died
        
    #detecting sleep
        if not (alarmTime < 0) : #alarm Control needed
            if( gpDetection.is_alive()  == True ) : #detection is working now, turn off detection process
                    gStreamingAddr = gBaseStreamAddr
                    gpDetection.terminate() 
                    time.sleep(2) #neccessary, waiting Process died
                
            if not (alarmMode == 0) :  #need detection
                # hostip = gNetWorkManager.GethostIP()
                hostip = gNetWorkManager.GethostIP() 
                gStreamingAddr = utils.ConcatStr('http://',[hostip,':5000','/vid'])
                gFace_detector = cFaceDetector(alarm_mode = alarmMode,alarm_time = alarmTime)
                if(strmRequest==True):
                    gpDetection = Process(target=gpApp.run, kwargs={"host":hostip,"port":'5000',"debug":False, "threaded":True})
                else:
                    gpDetection = Process(target=gFace_detector.dectecing_face_alarm)
                    
                gpDetection.start()
    
            NowStreamingAddr = gStreamingAddr
            sendingData = {"5" : NowStreamingAddr}
            result , packet = gPacketManager.MakingPacketToSend(sendingData)

            if(result == False) : 
                print("StreamingError!")
                exit()

        #send Packet
        if __debug__ :
            print("senddata: " ,packet)
        gNetWorkManager.SendAll(packet)

        time.sleep(1)

 ####

