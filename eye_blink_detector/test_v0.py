## 정상으로 작동
# closed_limit 하기 전
import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
import time
from flask import Flask, Response, render_template

IMG_SIZE = (34, 26)
app = Flask(__name__)
frame_width = 640
frame_height = 480
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

model = load_model('models/2018_12_17_22_58_35.h5')
#model.summary()

def crop_eye(img, eye_points):
  x1, y1 = np.amin(eye_points, axis=0)
  x2, y2 = np.amax(eye_points, axis=0)
  cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

  w = (x2 - x1) * 1.2
  h = w * IMG_SIZE[1] / IMG_SIZE[0]

  margin_x, margin_y = w / 2, h / 2

  min_x, min_y = int(cx - margin_x), int(cy - margin_y)
  max_x, max_y = int(cx + margin_x), int(cy + margin_y)

  eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

  eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

  return eye_img, eye_rect

# main
#cap = cv2.VideoCapture(0)

# while cap.isOpened(): # 기존꺼. 안씀
#   ret, img_ori = cap.read()

#   if not ret:
#     break

#   img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

#   img = img_ori.copy()
#   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#   faces = detector(gray)

#   for face in faces:
#     shapes = predictor(gray, face)
#     shapes = face_utils.shape_to_np(shapes)

#     eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
#     eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

#     eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
#     eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
#     eye_img_r = cv2.flip(eye_img_r, flipCode=1)

#     cv2.imshow('l', eye_img_l)
#     cv2.imshow('r', eye_img_r)

#     eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
#     eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

#     pred_l = model.predict(eye_input_l)
#     pred_r = model.predict(eye_input_r)

#     # visualize
#     state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
#     state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'

#     state_l = state_l % pred_l
#     state_r = state_r % pred_r

#     cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
#     cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,255,255), thickness=2)

#     cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
#     cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

#   cv2.imshow('result', img)
#   if cv2.waitKey(1) == ord('q'):
#     break

############
status = 'Awake'
number_closed = 0
#closed_limit = 10 #-- 눈 감김이 10번 이상일 경우 졸음으로 간주
show_frame = None
sign = None
color = None
def gen_frames():
    global number_closed
    global color
    global show_frame
    global sign

    cap = cv2.VideoCapture(0)
    cap.set(3, frame_width)
    cap.set(4, frame_height)

    while True:
        ret, img_ori = cap.read()
        if not ret:
            break
        img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)
        img = img_ori.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
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

            state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'
            state_l = state_l % pred_l
            state_r = state_r % pred_r

            cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
            cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,255,255), thickness=2)
            cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        # 프레임을 JPEG 형식으로 인코드합니다.
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tostring()

        # M-JPEG 스트리밍 형식에 맞게 프레임을 반환합니다.
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + frame + b'\r\n')        

    # 카메라를 정리합니다.
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vid')
def vid():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.0.79', port="5000", debug=False, threaded=True)