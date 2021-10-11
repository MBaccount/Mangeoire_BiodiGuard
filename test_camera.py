import numpy as np
import cv2 as cv

print("TRouble")
#cap=cv.VideoCapture(0)
cap=cv.VideoCapture(1)
print("TRouble")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    print("It's open")
while True:
    ret,frame=cap.read()
    if not ret:
        print("Can't receive frame. Exiting")
        break
    cv.imwrite('/home/pi/Desktop/camera2.jpg',frame)

cap.release()
cv.destroyAllWindows()