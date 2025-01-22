import cv2 as cv
import time
import numpy as np
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1] # -64
volBar = 400
volPercent = 0

# When program ends, set volume back to original level
return_to_og_volume = volume.GetMasterVolumeLevel()



# Setup for camera capture
cap = cv.VideoCapture(0)
image_width = 640
image_height = 480
cap.set(3, image_width)
cap.set(4, image_height)

# Used in displaying FPS
pTime = 0

# Determines whether to quit program
quit = False

# Setup for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as hands:
        while not quit:
            ret, frame = cap.read()

            # flips image and converts it from BGR to RGB
            frame = cv.flip(frame,1)
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # X and Y pos for fingers
                    x_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
                    y_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                    x_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width
                    y_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
                    x_ring = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image_width
                    y_ring = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height

                    # Midpoint x and midpoint y between index and thumb
                    mid_x, mid_y = (x_index + x_thumb) // 2, (y_index + y_thumb) // 2

                    # Index to thumb length, index to ring length
                    itlength = math.hypot(x_thumb - x_index, y_thumb - y_index)
                    irlength = math.hypot(x_thumb - x_ring, y_thumb - y_ring)

                    # Draws a circle on the thumb and middle fingers
                    cv.circle(frame, (int(x_index), int(y_index)), 15, (0,itlength,255-itlength), -1)
                    cv.circle(frame, (int(x_thumb), int(y_thumb)), 15, (0,itlength,255-itlength), -1)
                    # Draws a line between the thumb and middle fingers, along with a midpoint circle
                    cv.line(frame, (int(x_index), int(y_index)), (int(x_thumb), int(y_thumb)), (0,itlength,255-itlength), 3)
                    cv.circle(frame, (int(mid_x), int(mid_y)), 15, (0,itlength,255-itlength), -1)

                    # Interpolates itlength to our minVol and maxVol
                    vol = np.interp(itlength,[35,285],[minVol, maxVol])
                    volBar = np.interp(itlength,[35,285],[400, 150])
                    volPercent = np.interp(itlength,[35,285],[0, 100])

                    print(int(itlength), vol)
                    # Then set our volume level to this interpolation
                    volume.SetMasterVolumeLevel(vol, None)
                    
                    # If the distance between our index and ring fingers is less than 30 pixel,
                    # quit the program. This only runs if our index to thumb length is greater
                    # than 50 pixels, to ensure the program doesn't accidentally quit when changing volume.
                    if int(irlength) < 30 and int(itlength) > 60:
                        quit = True
                    
            cv.rectangle(frame, (50,150), (85,400), (0,255,0), 3)
            cv.rectangle(frame, (50, int(volBar)), (85,400), (0,255,0), cv.FILLED)
                         
            # Some calculations to display the current FPS on screen
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv.putText(frame, f"FPS: {int(fps)}", (25,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2, cv.LINE_AA)
            cv.putText(frame, f"{int(volPercent)}%", (45,433), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2, cv.LINE_AA)

            # Show our final image, update every 1ms
            cv.imshow("Tracking", frame)
            cv.waitKey(1)

# Return to OG volume on exit
volume.SetMasterVolumeLevel(return_to_og_volume, None)