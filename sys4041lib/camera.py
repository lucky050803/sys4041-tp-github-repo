# LIB DISCONTINUED FOR NOW
# POC SHOWED PERFORMANCE PROBLEMS ON TARGET PLATFORM
# DO NOT USE
#######################################################

import Picamera2

# UNTESTED
def init_camera() :

    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (480, 368)},controls={'FrameRate': 60, 'FrameDurationLimits': (100, 50000)}, buffer_count=1))
        picam2.start()
    except Exception as e:
        print("Can't start camera. Is it plugged in ? Is there another process using it ?")
        print("Error:", str(e))
        exit(1)

    time.sleep(2.0)
