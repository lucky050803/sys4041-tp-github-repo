# LIB DISCONTINUED FOR NOW
# POC SHOWED PERFORMANCE PROBLEMS ON TARGET PLATFORM
# DO NOT USE
#######################################################

import cv2
import time
import numpy as np
import datetime

# TODO simplify to return only position + size
def get_markers(image):
    print('hey')
    start = time.time()

    output = []

    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    arucoParams = cv2.aruco.DetectorParameters_create()

    # Normalizing image according to lens parameters
    marker_length = 0.053 # [m]
    camera_matrix = np.array([[673.9683892, 0., 343.68638231],[0., 676.08466459, 245.31865398],[0., 0., 1.]])
    distortion_coeff = np.array([5.44787247e-02, 1.23043244e-01, -4.52559581e-04, 5.47011732e-03, -6.83110234e-01])

    # Aruco detection
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        print(corners)
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))


            ret = cv2.aruco.estimatePoseSingleMarkers(markerCorner, marker_length, camera_matrix, distortion_coeff)
            (rvec, tvec) = (ret[0][0, 0, :], ret[1][0, 0, :])
            #Supprimer les axes inutiles
            tvec = np.squeeze(tvec)
            rvec = np.squeeze(rvec)
            #Conversion de vecteur de rotation en origines
            rvec_matrix = cv2.Rodrigues(rvec)
            rvec_matrix = rvec_matrix[0] #Extrait de rodorigues
            #Traduction du vecteur translationnel
            transpose_tvec = tvec[np.newaxis, :].T
            #Synthétique
            proj_matrix = np.hstack((rvec_matrix, transpose_tvec))
            #Conversion en angle d'Euler
            euler_angle = cv2.decomposeProjectionMatrix(proj_matrix)[6] # [deg]
            x = int(100*tvec[0])
            y = int(100*tvec[1])
            z = int(64*tvec[2])#correction suite à des mesures reélles
            pitch = int(euler_angle[1][0])
            yaw = int(euler_angle[2][0])
            roll = int(euler_angle[0][0])

            print({"x": type(x), "y": type(y), "z": type(z), "pitch": type(pitch), "yaw": type(yaw), "roll": type(roll), "id": type(markerID)})

            output.append({"x": x, "y": y, "z": z, "pitch": pitch, "yaw": yaw, "roll": roll, "id": int(markerID)})

    return {"markers": output, "time": time.time() - start}

# TODO
def get_marker_count(image) :
    return ''
