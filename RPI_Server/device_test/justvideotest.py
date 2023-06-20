import cv2

cap = cv2.VideoCapture(0)
# if cap.isOpened():
#     print('open~~~')
while True:
    ret, frame = cap.read()
    # print(frame)

    if not ret:
        print('wrong')
        break
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xFF
    if (key == 27): 
        break