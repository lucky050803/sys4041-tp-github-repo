# DISCONTINUED FOR NOW
# POC SHOWED PERFORMANCE PROBLEMS ON TARGET PLATFORM
# DO NOT USE
#######################################################

# Simple testing for aruco recognition with Flask streaming support

from picamera2 import Picamera2
import argparse
import datetime
import time
import cv2
import threading

from flask import Response
from flask import Flask
from flask import render_template

#from sys4041lib.aruco import get_markers
from aruco import get_markers 



# Init flask
outputFrame = None
lock = threading.Lock()
app = Flask(__name__)

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


# Serving the frames
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

# Main aruco recognition thread
def aruco_t() :
    global outputFrame

    while(True) :
        raw_image = picam2.capture_array()
        image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        image = cv2.rotate(image, cv2.ROTATE_180)

        print(get_markers(image))
        time.sleep(.3)

        with lock:
            outputFrame = image.copy()

if __name__ == '__main__':
    # start a thread that will perform motion detection
    t = threading.Thread(target=aruco_t, args=())
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host='0.0.0.0', port=8000, debug=True,
        threaded=True, use_reloader=False)
