#OpenCV_test_3.py

# this program tracks a red ball
# (no motor control is performed to move the camera, we will get to that later in the tutorial)

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import os




# initialize the camera and grab a reference to the raw camera capture
capWebcam = PiCamera()
capWebcam.resolution = (640, 480)
capWebcam.framerate = 32
rawCapture = PiRGBArray(capWebcam, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in capWebcam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	imgOriginal = frame.array


 
        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        imgThreshLow = cv2.inRange(imgHSV, np.array([0, 135, 135]), np.array([18, 255, 255]))
        imgThreshHigh = cv2.inRange(imgHSV, np.array([165, 135, 135]), np.array([179, 255, 255]))

        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)

        imgThresh = cv2.dilate(imgThresh, np.ones((5,5),np.uint8))
        imgThresh = cv2.erode(imgThresh, np.ones((5,5),np.uint8))

        intRows, intColumns = imgThresh.shape

        circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 5, intRows / 4)      # fill variable circles with all circles in the processed image

        if circles is not None:                     # this line is necessary to keep program from crashing on next line if no circles were found
            for circle in circles[0]:                           # for each circle
                x, y, radius = circle                                                                       # break out x, y, and radius
                print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)       # print ball position and radius
                cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)           # draw small green circle at center of detected object
                cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)                     # draw red circle around the detected object
            # end for
        # end if

        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)            # create windows, use WINDOW_AUTOSIZE for a fixed window size
        cv2.namedWindow("imgThresh", cv2.WINDOW_AUTOSIZE)           # or use WINDOW_NORMAL to allow window resizing

        cv2.imshow("imgOriginal", imgOriginal)                 # show windows
        cv2.imshow("imgThresh", imgThresh)
        key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
