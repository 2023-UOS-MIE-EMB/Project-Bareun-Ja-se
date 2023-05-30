import cv2, dlib, time
from flask import Flask, Response, render_template
#
App = Flask(__name__)
HostIP = '172.16.63.142'
FrameWidth = 640
FrameHeight = 480

FaceDetectModel = dlib.get_frontal_face_detector()

gFrameDisplayingonWeb = None
gCountDenotation = None
gStatusColor = None
gCameraPort = 0
# gWorkingTime -> gSleepingTime -> gWorkingTime -> gSleepingTime ... 루프가 반복되는 방식
gWorkingTime = 15 # 시간(초)동안 얼굴 인식을 실행
gAlarmTime = 5 # 시간(초) 동안 얼굴이 없는 경우에 알람. gAlarmTime은 gWorkingTime보다 크면 안됨
gSleepingTime = 2 # 시간(초) 동안 while 문을 멈춤
gfaceList = [] # 얼굴 유무를 담을 list. 얼굴없음(-1)과 얼굴탐지(1)이 들어감

'''
@기능
    웹캠을 이용하여 얼굴을 감지하고, 이를 웹 페이지에 실시간으로 스트리밍한다. 
    얼굴이 연속적으로 감지되지 않은 경우를 추적하여 사용자가 졸고 있는지 판단하는 기능도 포함하고 있다.'''
def DetectingFaceForStreaming():
    global gStatusColor
    global gFrameDisplayingonWeb
    global gCountDenotation
    global gWorkingTime 
    global gAlarmTime
    global gSleepingTime 
    global gfaceList
    global gCameraPort
    Camera = cv2.VideoCapture(gCameraPort)
    Camera.set(3, FrameWidth)
    Camera.set(4, FrameHeight)

    StartAlarmTime = StartgWorkingTime = time.time() # gWorkingTime 계산을 위한 시작 시간
    while True:
        if (time.time() - StartgWorkingTime) < gWorkingTime: #gWorkingTime 시간 동안
            elapsedTime = time.time() - StartAlarmTime 

            if elapsedTime < gAlarmTime: # gAlarmTime동안에는 얼굴탐지
                Success, FrameForFaceDetect = Camera.read()
                if not Success:
                    break
                gFrameDisplayingonWeb = FrameForFaceDetect
                GrayFrame = cv2.cvtColor(FrameForFaceDetect, cv2.COLOR_BGR2GRAY)
                GrayFrame = cv2.equalizeHist(GrayFrame)            
                faces = FaceDetectModel(GrayFrame)
                if len(faces) == 0: 
                    UserStatus = 'Sleep'
                    gStatusColor = (0, 0, 255)
                    gfaceList.append(-1) # 얼굴이 없으면 -1을 list에 추가
                    cv2.putText(gFrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, gStatusColor, 2)
                    print('no face')
                else: 
                    UserStatus = 'Awake'
                    gStatusColor = (0, 255, 0)
                    gfaceList.append(1) # 얼굴이 있으면 1을 list에 추가
                    cv2.putText(gFrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, gStatusColor, 2)
                    print('face detected')

                _, buffer = cv2.imencode('.jpg', gFrameDisplayingonWeb)
                frame = buffer.tostring()
                yield (b'--frame\r\n'
                    b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')
            else: #(elapsedTime > gAlarmTime)  gAlarmTime이 지나면 최종 판단
                # gWorkingTime이 지나면, list에 있는 값을 합하여 얼굴 유무 판단
                faceCount = sum(gfaceList)  #졸음이 더 많으면 음수, 얼굴인식이 더 많으면 양수가 됨
                gfaceList.clear()
                if faceCount < 0:
                    UserStatus = 'Sleep'
                    gStatusColor = (0, 0, 255)
                    # 졸음을 깨우는 코드 이곳에 작성
                else:
                    UserStatus = 'Awake'
                    gStatusColor = (0, 255, 0)
                print('Final: ',UserStatus)
                cv2.putText(gFrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 2, gStatusColor, 2)
                _, buffer = cv2.imencode('.jpg', gFrameDisplayingonWeb)
                frame = buffer.tostring()
                yield (b'--frame\r\n'
                    b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')
                # 시간 초기화 후 다음 StartAlarmTime을 위해 다시 시작
                StartAlarmTime = time.time()
        
        else: #gSleepingTime 동안 sleep
            print('sleeping...zzz')
            time.sleep(gSleepingTime)
            StartAlarmTime = StartgWorkingTime = time.time()
    del (Camera)

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/vid')
def vid():
    return Response(DetectingFaceForStreaming(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    App.run(host=HostIP, port="5000", debug=False, threaded=True)
