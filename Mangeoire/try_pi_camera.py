import picamera
from time import sleep

camera = picamera.PiCamera()

camera.capture('/home/pi/image1.jpg')
sleep(5)
camera.capture('/home/pi/image2.jpg')