from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import sys
import thread
import serial

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

# Open the serial port.
ser = serial.Serial('/dev/ttyACM0')

# Flag for quitting the process.
quit = False

# List of robot times recorded for image frames.
robot_times = []

def quitting_time():
    global quit
    in_string = raw_input('Enter "q" to stop recording.')
    if in_string == "q":
        quit = True

thread.start_new_thread(quitting_time, ())

def get_time_str(ser_obj):
    """ Function to get the current time from the Neato robot.
        This only works with a special version of the robot
        software which returns a string such as:
        robot_time_ms, 123456.789
        when the gettime command is given.
        :param ser_obj: The serial object used to talk to the
                        robot.
        :returns: The parsed time string from the robot with
                  newline character.
    """
    # Get time.
    ser_obj.write('gettime\r')

    # Flush buffer until we get the correct token.
    line_tok = ['start']
    while line_tok[0] != 'robot_time_ms':
       	line = ser.readline()
       	line_tok = line.split(',')
    
    # Read time data.
    time_in_ms = line_tok[1]

    return time_in_ms 

# Main function.
# Tell the robot to clean.
ser.write('clean\r')

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the robot time to associate with the frame.
    robot_times.append(get_time_str(ser))
	
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

# Close serial port.
ser.close()

# Write the times to a file.
robot_time_log = open('robot_times.csv', 'w')
for robot_time in robot_times:
    robot_time_log.write("%s" % robot_time)
