import cv2, dlib
from flask import Flask, Response, render_template
import time 

App = Flask(__name__)
HostIP = '172.16.63.142'
FrameWidth = 640
FrameHeight = 480

FaceDetectModel = dlib.get_frontal_face_detector()

gCountNoFaceDetected = 0    
gUpperBoundofFaceCount = 10 #얼굴이 10번 이상 감지되지 않을 경우 졸음으로 간주
gFrameDisplayingonWeb = None
gCountDenotation = None
gStatusColor = None

'''
@기능
    웹캠을 이용하여 얼굴을 감지하고, 이를 웹 페이지에 실시간으로 스트리밍한다. 
    얼굴이 연속적으로 감지되지 않은 경우를 추적하여 사용자가 졸고 있는지 판단하는 기능도 포함하고 있다.'''
def DetectingFaceForStreaming():
    global gCountNoFaceDetected
    global gStatusColor
    global gFrameDisplayingonWeb
    global gCountDenotation
    global gUpperBoundofFaceCount
    CameraPort = 0
    Camera = cv2.VideoCapture(CameraPort)
    Camera.set(3, FrameWidth)
    Camera.set(4, FrameHeight)

    FaceDetectionIntervalTime = 1 # seconds
    NextDetectionTime = time.time()

    while True:
        Success, FrameForFaecDetect = Camera.read()
        if not Success:
            break

        gFrameDisplayingonWeb = FrameForFaecDetect

        if time.time() > NextDetectionTime:
            NextDetectionTime = time.time() + FaceDetectionIntervalTime

            GrayFrame = cv2.cvtColor(FrameForFaecDetect, cv2.COLOR_BGR2GRAY)
            GrayFrame = cv2.equalizeHist(GrayFrame)            
            faces = FaceDetectModel(GrayFrame)
            if len(faces) == 0: 
                if gCountNoFaceDetected < gUpperBoundofFaceCount:
                    gCountNoFaceDetected += 1
                UserStatus = 'Sleep'
                gStatusColor = (0, 0, 255)

            else: 
                face = faces[0] #하나의 얼굴만 탐지
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y
                cv2.rectangle(gFrameDisplayingonWeb, (x, y), (x+w, y+h), (50, 200, 0), 2)
                
                gCountNoFaceDetected = max(0, gCountNoFaceDetected - 1)
                UserStatus = 'Awake'
                gStatusColor = (0, 255, 0)
                    
        gCountDenotation = 'No face count : ' + str(gCountNoFaceDetected) + ' / ' + str(gUpperBoundofFaceCount)

        cv2.putText(gFrameDisplayingonWeb, UserStatus , (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, gStatusColor, 2)
        cv2.putText(gFrameDisplayingonWeb, gCountDenotation , (10,FrameHeight-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, gStatusColor, 2)
            
        _, buffer = cv2.imencode('.jpg', gFrameDisplayingonWeb)
        frame = buffer.tostring()

        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')

    del (Camera)

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/vid')
def vid():
    return Response(DetectingFaceForStreaming(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    App.run(host=HostIP, port="5000", debug=False, threaded=True)
