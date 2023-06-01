from multiprocessing import Queue
import time
import random
from facedetect_module import cFaceDetector
import socket
from flask import Flask, Response
import utils

App = Flask(__name__)
face_detector = cFaceDetector()

'''
@기능
    졸음 인식을 실시하고 그에 따라 알람을 울리는 작업을 수행. 인식과 동시에 스트리밍 서버 주소를 
    공유 메모리 공간인 Queue에 넣는다.
@인자
    -alarmTime : 알람을 울리는데 기준이 되는 시간
    -alramMode : 비트마스크를 통해 4가지 알람방식(진동/소리/둘다/무음)을 나타낸다.
    
@OUT
    -streamingAddr  :  다른 프로세스와 공유할 '스트리밍 웹주소 str' 을 넣는 Q '''
def Detection( alarmTime :int , alarmMode : int , streamingAddr : Queue):
    global face_detector
    streamingAddr.cancel_join_thread()
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    hostip = s.getsockname()[0]
    s.close()
    face_detector = cFaceDetector(alarm_time = alarmTime, alarm_mode = alarmMode)

    strmAddr = utils.ConcatStr(hostip,'/vid')
    streamingAddr.put(strmAddr)
    
    App.run(host=hostip, port="5000", debug=False, threaded=False)

    

    # while(1):
    #     #todo
    #     #1.start recognization
    #     #2.put streaming web ip to streamingAddr 
    #     print("detecing...")
    #     #for test
    #     tmpAddr = str(random.randint(0,4000))

    #     streamingAddr.put(tmpAddr)
    #     time.sleep(2)

@App.route('/vid')
def vid():
    global face_detector
    return Response(face_detector.detecting_face_for_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')