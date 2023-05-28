import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
import time
from flask import Flask, Response, render_template

MODE = 'Streaming'
#MODE = 'Debug'
#MODE = 'Deamon'

IMG_SIZE = (34, 26)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = load_model('models/2018_12_17_22_58_35.h5')

frame_width = 640
frame_height = 480
number_closed = 0
closed_limit = 5 #-- 눈 감김이 해당 개수 이상일 경우 졸음으로 간주하여 사용자를 깨움
show_frame = None
sign = None
color = (0,255,0) 

def crop_eye(img, eye_points):
  x1, y1 = np.amin(eye_points, axis=0)
  x2, y2 = np.amax(eye_points, axis=0)
  cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

  w = (x2 - x1) * 1.2
  h = w * IMG_SIZE[1] / IMG_SIZE[0]

  margin_x, margin_y = w / 2, h / 2

  min_x, min_y = int(cx - margin_x), int(cy - margin_y)
  max_x, max_y = int(cx + margin_x), int(cy + margin_y)

  eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(int)
  eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

  return eye_img, eye_rect


def SleepDetect_streaming(): # 졸음탐지를 해서 웹페이지에서 스트리밍하기 위한 함수
    global number_closed
    global show_frame
    global sign
    global color

    cap = cv2.VideoCapture(0)
    cap.set(3, frame_width)
    cap.set(4, frame_height)

    while True:
        ret, img_ori = cap.read()
        if not ret:
            break
        #img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)
        show_frame = img_ori.copy()
        gray = cv2.cvtColor(show_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) == 0:
            status = 'No Face'
            color = (255,0,255) # 보라색
        else:
            face = faces[0] #하나의 얼굴만 탐지
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)
            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            pred_l = model.predict(eye_input_l)
            pred_r = model.predict(eye_input_r)
    
            # 두 눈 모두 감겼다고 예측된 경우 'sleep' 상태로, 그렇지 않은 경우 'awake' 상태로 설정합니다.
            if pred_l <= 0.3 and pred_r <= 0.3:
                status = 'sleep'
                color = (0,0,255) #눈 박스를 빨간색으로 바꿈
                number_closed = min(closed_limit+10, number_closed + 1)  # 눈 감은 횟수 증가, 단, closed_limit+10을 넘지 않도록 합니다.
            else:
                status = 'Awake'
                color = (0,255,0) #눈 박스를 초록색으로 바꿈
                number_closed = max(0, number_closed - 1)  # 눈 뜬 횟수 증가, 단, 0 미만으로 내려가지 않도록 합니다.
            sign = 'sleep count : ' + str(number_closed) + ' / ' + str(closed_limit)

            
            # 왼쪽과 오른쪽 각각 예측값 화면에 띄우는 코드. (나중에 지워도 될듯)
            state_l = '(%.1f)' if pred_l > 0.1 else '(%.1f)'
            state_r = '(%.1f)' if pred_r > 0.1 else '(%.1f)'
            state_l = state_l % pred_l
            state_r = state_r % pred_r
                
            cv2.rectangle(show_frame, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=color, thickness=2)
            cv2.rectangle(show_frame, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=color, thickness=2)
            cv2.putText(show_frame, state_l, tuple(eye_rect_l[0:2]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
            cv2.putText(show_frame, state_r, tuple(eye_rect_r[0:2]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        
        # 졸음 확정시 알람 설정
        if( number_closed >= closed_limit ):
            show_frame = gray
            cv2.putText(show_frame, "Sleeping", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 2)        
        cv2.putText(show_frame, status , (500,50), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
        cv2.putText(show_frame, sign , (30,440), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255,255,255), 2)
           
        # 프레임을 JPEG 형식으로 인코드합니다.
        ret, buffer = cv2.imencode('.jpg', show_frame)
        frame = buffer.tobytes()
        #frame = buffer.tostring()

        # M-JPEG 스트리밍 형식에 맞게 프레임을 반환합니다.
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')        

    # 카메라를 정리합니다.
    cap.release()

def SleepDetect_imshow():  #웹페이지에서 스트리밍 없이 리눅스 GUI에서 졸음탐지하는 함수
    global number_closed
    global show_frame
    global sign
    global color

    cap = cv2.VideoCapture(0)
    cap.set(3, frame_width)
    cap.set(4, frame_height)

    while True:
        ret, img_ori = cap.read()
        if not ret:
            break

        show_frame = img_ori.copy()
        gray = cv2.cvtColor(show_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) == 0:
            status = 'No Face'
            color = (255,0,255)
        else:
            face = faces[0]
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)

            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)

            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

            pred_l = model.predict(eye_input_l)
            pred_r = model.predict(eye_input_r)

            if pred_l <= 0.3 and pred_r <= 0.3:
                status = 'Sleep'
                color = (0,0,255)
                number_closed = min(closed_limit+10, number_closed + 1)
            else:
                status = 'Awake'
                color = (0,255,0)
                number_closed = max(0, number_closed - 1)

            sign = 'Sleep count : ' + str(number_closed) + ' / ' + str(closed_limit)
            state_l = '(%.1f)' if pred_l > 0.1 else '(%.1f)'
            state_r = '(%.1f)' if pred_r > 0.1 else '(%.1f)'

            state_l = state_l % pred_l
            state_r = state_r % pred_r

            cv2.rectangle(show_frame, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=color, thickness=2)
            cv2.rectangle(show_frame, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=color, thickness=2)

            cv2.putText(show_frame, state_l, tuple(eye_rect_l[0:2]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
            cv2.putText(show_frame, state_r, tuple(eye_rect_r[0:2]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)

        if number_closed >= closed_limit:
            cv2.putText(show_frame, "Sleeping", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 2)
        
        cv2.putText(show_frame, status , (500,50), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
        cv2.putText(show_frame, sign , (30,440), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255,255,255), 2)
        
        cv2.imshow("Frame", show_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def SleepDetect_daemon(verbose = False):  #웹페이지에서 스트리밍 없이 백그라운드에서 졸음탐지하는 함수 
    global number_closed
    global show_frame
    global sign
    global color

    cap = cv2.VideoCapture(0)
    cap.set(3, frame_width)
    cap.set(4, frame_height)

    while True:
        ret, img_ori = cap.read()
        if not ret:
            break

        show_frame = img_ori.copy()
        gray = cv2.cvtColor(show_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) == 0:
            status = 'No Face'
            # 얼굴을 인식못했다고 사용자에게 알리는 코드 여기에 작성하기
            if verbose: 
                print('No Face detected')
        else:
            face = faces[0]
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)
            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            pred_l = model.predict(eye_input_l)
            pred_r = model.predict(eye_input_r)

            if pred_l <= 0.3 and pred_r <= 0.3:
                status = 'Sleep'
                number_closed = min(closed_limit+10, number_closed + 1)
            else:
                status = 'Awake'
                number_closed = max(0, number_closed - 1)

            sign = 'Sleep count : ' + str(number_closed) + ' / ' + str(closed_limit) + '. Status is ' + status
            if verbose: 
                print(sign)
        
        if number_closed >= closed_limit:
            # 기준치를 넘겼으므로 사용자를 깨우는 코드 여기에 작성하기
            if verbose:
                print('########### Sleeping.... Wake up!!! ###########')

        #cv2.imshow("Frame", show_frame)

        # 다른 방식으로 데몬을 종료하는 방법 생각해봐야 함. 
        if cv2.waitKey(1) & 0xFF == ord('q'): #imshow 안하면 q키로 종료하는 것도 안됨
            break

    cap.release()
    cv2.destroyAllWindows()
 



print('Sleeping Detector Starting...')

if MODE == 'Streaming':
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/vid')
    def vid():
        return Response(SleepDetect_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')
    app.run(host='192.168.0.79', port="5000", debug=False, threaded=True)


elif MODE == 'Debug':
    SleepDetect_imshow()    

elif MODE == 'Deamon':
    SleepDetect_daemon(verbose = True)  #verbose = True이면 stdout으로 로깅