import cv2, dlib, time
from flask import Flask, Response, render_template
import socket
'''
@기능
    웹캠을 이용하여 얼굴을 감지하고, 이를 웹 페이지에 실시간으로 스트리밍한다. 
    얼굴이 연속적으로 감지되지 않은 경우를 추적하여 사용자가 졸고 있는지 판단하는 기능도 포함하고 있다.
@생성자
    FaceDetector(host_ip, camera_port, frame_width, frame_height, working_time, alarm_time, sleeping_time)
    - host_ip : 서버의 호스트 IP. Flask 어플리케이션이 실행되는 호스트를 설정하기 위한 값이다.
    - camera_port : 사용하고자 하는 카메라의 포트 번호. 카메라를 열기 위한 값이다.
    - frame_width, frame_height : 캡쳐할 프레임의 가로와 세로 크기. 웹캠에서 읽어올 이미지의 크기를 설정하기 위한 값이다.
    - working_time : 얼굴 감지를 실행하는 시간 (초). 
    - alarm_time : 얼굴이 없는 경우에 알람을 발생시키는 시간 (초). 이 값은 working_time보다 클 수 없다.
    - sleeping_time : 얼굴 감지를 중지하는 시간 (초).  
@주의사항
    alarm_time은 working_time보다 클 수 없다. sleeping_time 동안에는 얼굴 감지가 중지된다.
'''
class cFaceDetector:

    def __init__(self, host_ip='127.0.0.1', camera_port=0, frame_width=320, frame_height=240, 
                 working_time=15, alarm_time=5,alarm_mode=0, sleeping_time=2):

        self.FaceDetectModel = dlib.get_frontal_face_detector()

        self.FrameDisplayingonWeb = None
        self.StatusColor = None

        self.host_ip = host_ip
        self.CameraPort = camera_port
        self.FrameWidth = frame_width
        self.FrameHeight = frame_height

        self.WorkingTime= working_time
        self.AlarmTime = alarm_time
        self.SleepingTime = sleeping_time
        self.AlarmMode = alarm_mode

        self.FaceList = [] # 얼굴 유무를 담을 list. 얼굴없음(-1)과 얼굴탐지(1)이 들어감
    
    def detecting_face_for_streaming(self):

        print("time:", self.AlarmTime)
        check_Sleeep = 0

        Camera = cv2.VideoCapture(self.CameraPort)
        Camera.set(3, self.FrameWidth)
        Camera.set(4, self.FrameHeight)
        #print("time : ", self.AlarmTime )
        StartAlarmTime = StartWorkingTime = time.time() # WorkingTime 계산을 위한 시작 시간
        while True:
            if (time.time() - StartWorkingTime) < self.WorkingTime: # WorkingTime 시간 동안
                elapsedTime = time.time() - StartAlarmTime 

                if elapsedTime < self.AlarmTime: # AlarmTime 동안에는 얼굴탐지
                    Success, FrameForFaceDetect = Camera.read()
                    if not Success:
                        break
                    self.FrameDisplayingonWeb = FrameForFaceDetect
                    GrayFrame = cv2.cvtColor(FrameForFaceDetect, cv2.COLOR_BGR2GRAY)
                    GrayFrame = cv2.equalizeHist(GrayFrame)            
                    faces = self.FaceDetectModel(GrayFrame)
                    if len(faces) == 0: 
                        UserStatus = 'Undetected'
                        self.StatusColor = (0, 0, 255)
                        #self.FaceList.append(-1) # 얼굴이 없으면 -1을 list에 추가
                        check_Sleeep -= 1
                        cv2.putText(self.FrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, self.StatusColor, 2)
                        #print('no face')
                    else:
                        for face in faces: 
                            x = face.left()
                            y = face.top()
                            w = face.right() #-x
                            h = face.bottom() #- y
                            cv2.rectangle(self.FrameDisplayingonWeb,(x,y),(w,h),(50,200,0),2)

                        UserStatus = 'Detected'
                        self.StatusColor = (0, 255, 0)
                        #self.FaceList.append(1) # 얼굴이 있으면 1을 list에 추가
                        check_Sleeep += 1
                        cv2.putText(self.FrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, self.StatusColor, 2)
                        #print('face detected')

                    _, buffer = cv2.imencode('.jpg', self.FrameDisplayingonWeb)
                    frame = buffer.tostring()
                    yield (b'--frame\r\n'
                        b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')
                else: # (elapsedTime > AlarmTime)  AlarmTime이 지나면 최종 판단
                    #faceCount = sum(self.FaceList)  # 졸음이 더 많으면 음수, 얼굴인식이 더 많으면 양수가 됨
                    #self.FaceList.clear()
                    if check_Sleeep < 0:
                        UserStatus = 'Sleep'
                        self.StatusColor = (0, 0, 255)
                    else:
                        UserStatus = 'Awake'
                        self.StatusColor = (0, 255, 0)
                    check_Sleeep = 0

                    #print('Final: ',UserStatus)
                    #ring alarm
                    cv2.putText(self.FrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 2, self.StatusColor, 2)
                    _, buffer = cv2.imencode('.jpg', self.FrameDisplayingonWeb)
                    frame = buffer.tostring()
                    yield (b'--frame\r\n'
                        b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')
                    # 시간 초기화 후 다음 StartAlarmTime을 위해 다시 시작
                    StartAlarmTime = time.time()
            
            else: # SleepingTime 동안 sleep
                print('sleeping...zzz')
                time.sleep(self.SleepingTime)
                StartAlarmTime = StartWorkingTime = time.time()
        del (Camera)


App = Flask(__name__)

face_detector = cFaceDetector()

# @App.route('/')
# def index():
#     return render_template('index.html')

#todo:
'''
dlt comment
adding ring
system 구상도 그리기

'''

if __name__ == '__main__':
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    hostip = s.getsockname()[0]
    s.close()
    App.run(host=hostip, port="5000", debug=False, threaded=True)
