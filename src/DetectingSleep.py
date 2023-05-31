from multiprocessing import Queue
import time
import random

import socket
from facedetect_module import cFaceDetector
from flask import Flask, Response, render_template

import subprocess

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
    # global App
    streamingAddr.cancel_join_thread()

    # App.run(host=face_detector.host_ip, port="5000", debug=False, threaded=True)

    #need to test after terminated 
    subprocess.Popen(["facedetect_module.py", ]) 

    while(1):
        #todo
        #1.start recognization
        #2.put streaming web ip to streamingAddr 
        print("detecing...")
        #for test
        tmpAddr = str(random.randint(0,4000))

        streamingAddr.put(tmpAddr)
        time.sleep(2)

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/vid')
def vid():
    return Response(face_detector.detecting_face_for_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')