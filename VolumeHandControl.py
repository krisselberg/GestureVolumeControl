import cv2
import time
import numpy as np
from HandTrackingModule import handDetector
import math
# volume functionality import
import osascript
code, out, err = osascript.run("output volume of (get volume settings)")
minVol = 0
maxVol = 100
vol = 0
volBar = np.interp(out, [0, 100], [400, 150])
volPer = out
print(out)

# Parameters
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
prevTime = 0

detector = handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2] # thumb coordinates
        x2, y2 = lmList[8][1], lmList[8][2] # pointer finger coordinates
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # center between thumb and pointer

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Hand range 20 - 280
        # Volume Range 0 - 100
        vol = np.interp(length, [20, 280], [minVol, maxVol])
        volBar = np.interp(length, [20, 280], [400, 150])
        volPer = np.interp(length, [20, 280], [0, 100])
        osascript.run("set volume output volume {}".format(vol))

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # display volume and volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # display fps and video feed
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 0), 3)
    cv2.imshow("Img", img)

    cv2.waitKey(1)