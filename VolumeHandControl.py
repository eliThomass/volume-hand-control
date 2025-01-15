import cv2 as cv
import time
import numpy as np
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)




minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1] # -64


cap = cv.VideoCapture(0)
image_width = 640
image_height = 480
cap.set(3, image_width)
cap.set(4, image_height)
pTime = 0

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as hands:
        while True:
            ret, frame = cap.read()

            # flips image and converts it from BGR to RGB
            frame = cv.flip(frame,1)
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    x_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
                    y_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                    x_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width
                    y_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height

                    mid_x, mid_y = (x_index + x_thumb) // 2, (y_index + y_thumb) // 2
                    length = math.hypot(x_thumb - x_index, y_thumb - y_index)

                    cv.circle(frame, (int(x_index), int(y_index)), 15, (0,length,255-length), -1)
                    cv.circle(frame, (int(x_thumb), int(y_thumb)), 15, (0,length,255-length), -1)
                    cv.line(frame, (int(x_index), int(y_index)), (int(x_thumb), int(y_thumb)), (0,length,255-length), 3)
                    cv.circle(frame, (int(mid_x), int(mid_y)), 15, (0,length,255-length), -1)

                    vol = np.interp(length,[35,285],[minVol, maxVol])
                    print(int(length), vol)
                    volume.SetMasterVolumeLevel(vol, None)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv.putText(frame, f"FPS: {int(fps)}", (25,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2, cv.LINE_AA)


            cv.imshow("Tracking", frame)
            cv.waitKey(1)