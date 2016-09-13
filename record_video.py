import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
    print("Capture opened.")
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, -1)

        # write the flipped frame
        out.write(frame)

        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
	print("No frame received.")
        break

# Release everything if job is finished
cap.release()
out.release()
