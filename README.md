# Volume Hand Control
## A Computer Vision Project
This program utilizes **OpenCV, MediaPipe,** and **PyCaw** to track your hands through a connected webcam. By calculating the distance between your fingers, the program changes the volume on your computer. You will need a video capture device for this program.

## Dependenices

To install all needed dependencies do:
```
pip install opencv
pip install mediapipe
pip install pycaw
pip install numpy
```
## Using the Program

To change the system volume, pinch together your thumb and index finger. When fully pinched, system volume will be zero. When fully extended apart, system volume will be max.

To exit the program, simply pinch together your thumb and ring finger. (Keep your index finger not pinched)

***Note***: Depending on distance to the webcam, it may be hard to reach the minimum and maximum pixel values. It is recommended to have your hand closer rather than farther to the camera.

## Credit
For this project, I followed a tutorial on YouTube, which can be found [here](https://www.youtube.com/watch?v=9iEPzbG-xLE). Due to the age of the video, there are differences in the code due to MediaPipe having been updated since.

Thanks to user [AndreMiras](https://github.com/AndreMiras/pycaw) and their **pycaw** library, which was used to control system volume.

Thanks to the OpenCV, MediaPipe, and NumPy teams for their respective libraries.