# DISCONTINUED FOR NOW
# POC SHOWED PERFORMANCE PROBLEMS ON TARGET PLATFORM
# DO NOT USE
#######################################################

# Simple testing for aruco recognition

from picamera2 import Picamera2
import argparse
import datetime
import time
import cv2

#from sys4041lib.aruco import get_markers
from aruco import get_markers 

# Init cam
try:
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (480, 368)},controls={'FrameRate': 60, 'FrameDurationLimits': (100, 50000)}, buffer_count=1))
    picam2.start()
except Exception as e:
    print("Can't start camera. Is it plugged in ? Is there another process using it ?")
    print("Error:", str(e))
    exit(1)

time.sleep(2.0)

while(True) :
    raw_image = picam2.capture_array()
    image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    image = cv2.rotate(image, cv2.ROTATE_180)

    print(get_markers(image))
    time.sleep(.3)
