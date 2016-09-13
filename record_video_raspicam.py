from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import sys
import thread

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480) #640,480
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640,480)) #640,480

# allow the camera to warmup
time.sleep(0.1)

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,480))

# Flag for quitting the process.
quit = False

def quitting_time():
	global quit
	in_string = raw_input('Enter "q" to stop recording.')
	if in_string == "q":
		quit = True

thread.start_new_thread(quitting_time, ())

#capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	image = frame.array

	# Flip the image because the camera is upside down.
	image = cv2.flip(image, -1)

        # write the flipped frame
        out.write(image)
	sys.stdout.write('.')
	sys.stdout.flush()
	#clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	if quit:
		break

# Release everything if job is finished
out.release()
