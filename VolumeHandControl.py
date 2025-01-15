import cv2 as cv
import time
import numpy as np
import mediapipe as mp

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
pTime = 0

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            frame = cv.flip(frame,1)
            
            results = hands.process(frame)

            if results.multi_hand_landmarks:
              for hand_landmarks in results.multi_hand_landmarks:
                 mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv.putText(frame, f"FPS: {int(fps)}", (25,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2, cv.LINE_AA)


            cv.imshow("Tracking", frame)
            cv.waitKey(1)