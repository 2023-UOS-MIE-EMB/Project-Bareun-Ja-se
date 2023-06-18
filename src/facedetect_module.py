import cv2, dlib, time
from flask import Flask, Response, render_template
import socket
from typing import Tuple
from HardWareManager import cHardWareManager

'''
@기능
    웹캠을 이용하여 얼굴을 감지하고, 이를 웹 페이지에 실시간으로 스트리밍한다. 
    얼굴이 연속적으로 감지되지 않은 경우를 추적하여 사용자가 졸고 있는지 판단하는 기능도 포함하고 있다.
@생성자
    FaceDetector(host_ip, camera_port, frame_width, frame_height, alarm_time)
    - host_ip : 서버의 호스트 IP. Flask 어플리케이션이 실행되는 호스트를 설정하기 위한 값이다.
    - camera_port : 사용하고자 하는 카메라의 포트 번호. 카메라를 열기 위한 값이다.
    - frame_width, frame_height : 캡쳐할 프레임의 가로와 세로 크기. 웹캠에서 읽어올 이미지의 크기를 설정하기 위한 값이다.
    - alarm_time : 얼굴이 없는 경우에 알람을 발생시키는 시간 (초). 이 값은 working_time보다 클 수 없다.
    - alram_mode :  기본 알람 모드, 비트마스크 값이며 현재 1,2 만 가능.
@주의사항
    alarm_time은 working_time보다 클 수 없다. sleeping_time 동안에는 얼굴 감지가 중지된다.'''
class cFaceDetector:

    __HardWareManager = cHardWareManager()

    __FaceDetectModel = dlib.get_frontal_face_detector()

    __CameraPort    = None
    __FrameWidth    = None
    __FrameHeight   = None

    __AlarmTime     = None
    __AlarmMode     = None

    Camera = None

    def __init__(self, camera_port=0, frame_width=320, frame_height=240, 
                alarm_time=5, alarm_mode = 0):

        self.__FaceDetectModel = dlib.get_frontal_face_detector()

        Frame = None
        self.__CameraPort       = camera_port

        self.__FrameWidth       = frame_width
        self.__FrameHeight      = frame_height
       
        self.__AlarmTime        = alarm_time       
        self.__AlarmMode        = alarm_mode
    
    def GetHWmanager(self):
        return self.__HardWareManager

    '''
    @기능
        face_detecting에서 동작시간과 휴식시간을 리턴한다.
    @ret
        Tuple[int,int] : [실행시간,휴식시간] '''
    def __SetExTimers(self) -> Tuple[int,int]:
        WorkingTime = int(self.__AlarmTime *2)
        SleepingTime = int(self.__AlarmTime/5)
        
        return WorkingTime, 0
    '''
    @기능
        스트리밍 없이 얼굴인식으로 비집중 시간을 감지하고, 알람을 울린다.
        알람 시간 이상 얼굴이 인식되지 않으면, 알람 모드에 따라 알람을 울린다.
        Sleeping Time을 통해 일정 기간 휴식을 취할 수도 있으나 현재는 불필요하여 막아둔 상태이다.'''
    def dectecing_face_alarm(self):
        print("time:", self.__AlarmTime)
        self.__HardWareManager.resetAll()
        check_Sleep = 0
        count_threshold = 90
        status_threshold = count_threshold/3

        Camera = cv2.VideoCapture(self.__CameraPort)
        Camera.set(3, self.__FrameWidth)
        Camera.set(4, self.__FrameHeight)

        userState = 1 #Awake
        nowState = 1
        RecentTime = StartWorkingTime = time.time() # WorkingTime 계산을 위한 시작 시간
        WorkingTime, SleepingTime = self.__SetExTimers() #Sleeping TIme does not needed
        while(True):
            nowTime =  time.time()
            if((nowTime - StartWorkingTime) >= WorkingTime) :
                if __debug__:
                    print("sleeping")
                StartWorkingTime = time.time()
                continue

            else:    
                if((nowTime - RecentTime) > self.__AlarmTime and userState == 0):
                    #ring alarm
                    if __debug__:
                        print("ring alarm!")
                    self.__HardWareManager.RingFromMode(self.__AlarmMode,True)
                    userState = 1
                else:
                    Success, FrameForFaceDetect = Camera.read()
                    if not Success:
                        break
                    GrayFrame = cv2.cvtColor(FrameForFaceDetect, cv2.COLOR_BGR2GRAY)
                    GrayFrame = cv2.equalizeHist(GrayFrame)            
                    faces = self.__FaceDetectModel(GrayFrame)
                    if len(faces) == 0:
                        #can't detect any Face
                        check_Sleep = max(check_Sleep-1,-count_threshold)
                        if __debug__ : 
                            print(check_Sleep)
                        if(check_Sleep < 0 ):
                            self.__HardWareManager.RingLED(True)    #led ON
                        if(check_Sleep < -status_threshold) :
                            nowState = 0 #sleep
                        
                    else: #detectedFace
                        if __debug__:
                            StatusColor = (0,0,255)
                            cv2.putText(FrameForFaceDetect, "detected", (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, StatusColor, 2)
                        check_Sleep = min(check_Sleep+1,count_threshold)
                        if __debug__ : 
                            print(check_Sleep)
                        if(check_Sleep >= 0 ):
                            self.__HardWareManager.RingLED(False)    #led OFF
                        if(check_Sleep > status_threshold) :
                            nowState = 1 #awake
                            self.__HardWareManager.RingFromMode(self.__AlarmMode,False)
            
                    if(userState != nowState):
                        userState = nowState   #state 판단 내리고 바뀔때만 초기화
                        RecentTime = time.time()
        del(Camera)
    '''
    @기능
        얼굴 인식이 동작되는 영상을 Flask 프레임워크를 이용해 송출한다.'''
    def detecting_face_for_streaming(self):
        print("time:", self.__AlarmTime)
        self.__HardWareManager.resetAll()

        Camera = cv2.VideoCapture(self.__CameraPort)
        Camera.set(3, self.__FrameWidth)
        Camera.set(4, self.__FrameHeight)

        while True:
            Success, FrameForFaceDetect = Camera.read()
            if not Success:
                break
            RawFrame = FrameForFaceDetect
            GrayFrame = cv2.cvtColor(FrameForFaceDetect, cv2.COLOR_BGR2GRAY)
            GrayFrame = cv2.equalizeHist(GrayFrame)            
            faces = self.__FaceDetectModel(GrayFrame)
            if len(faces) == 0: 
                UserStatus = 'Undetected'
                self.__StatusColor = (0, 0, 255)
                cv2.putText(RawFrame, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, self.__StatusColor, 2)
            else:
                # draw rectangle on Faces
                for face in faces: 
                    x = face.left()
                    y = face.top()
                    w = face.right() #-x
                    h = face.bottom() #- y
                    cv2.rectangle(RawFrame,(x,y),(w,h),(50,200,0),2)

                UserStatus = 'Detected'
                self.__StatusColor = (0, 255, 0)
                cv2.putText(RawFrame, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, self.__StatusColor, 2)
            #streaming Video via 'Mjpeg over HTTP'
            _, buffer = cv2.imencode('.jpg', RawFrame)
            frame = buffer.tostring()
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')
        del(Camera)

#test#
if __name__ == '__main__':
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    hostip = s.getsockname()[0]
    s.close()
    App = Flask(__name__)
    face_detector = cFaceDetector()

    App.run(host=hostip, port="5000", debug=False, threaded=True)
