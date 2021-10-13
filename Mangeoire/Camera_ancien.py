#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Camera
import io
import time
import datetime
from picamera import PiCamera
import numpy as np
from threading import Thread

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

class Camera (Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.width = 1440 # use lower resolution for motion check
        self.height = 1080
        self.camera=PiCamera()
        self.threshold=60 # how much must the color value (0-255) change to be considered a change
        self.stream = io.BytesIO()
        self.step = 1  # use this to toggle where the image gets saved
        self.numImages = 1 # count number of images processed
        self.captureCount = 0
        self.data1=0 
        self.data2=0
        self.data3=0
        self.start()
       
    def photo (self,individu) :
        date_time=datetime.datetime.now()
        name= date_time.strftime("%m_%d_%Y__%H_%M_%S")
        self.camera.capture('/home/pi/Desktop/camera1'+name+individu+'.jpg')
        
    def film (self,individu):
        date_time=datetime.datetime.now()
        name= date_time.strftime("%m_%d_%Y__%H_%M_%S")
        self.camera.start_recording('/home/pi/Desktop/camera1'+name+individu+'.h264')
        time.sleep(5)
        self.camera.stop_recording()
    
    def set_resolution(self,x,y):
        self.camera.resolution=(x,y)
        self.width=x
        self.height=y

    def run(self):      
        while self.threshold > 0:
            self.presence=0
            print ('Capture ' , self.numImages)
            if self.step == 1:
                self.stream.seek(0)
                self.camera.capture(self.stream, 'rgba',True) # use video port for high speed
                self.data1= np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                self.step = 2
            else:
                self.stream.seek(0)
                self.camera.capture(self.stream, 'rgba',True)
                self.data2= np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                self.step = 1
                self.numImages = self.numImages + 1

            if self.numImages > 4:  # ignore first few images because if the camera is not quite ready it will register as motion right away
                    # look for motion unless we are in save mode
                if self.captureCount <= 0:
                       # print("Compare")
                        # not capturing, test for motion (very simplistic, but works good enough for my purposes)
                    self.data3 = np.abs(self.data1 - self.data2)  # get difference between 2 successive images
                    self.numTriggers = np.count_nonzero(self.data3 > self.threshold) / 4 / self.threshold #there are 4 times the number of pixels due to rgba

                        #print("Trigger cnt=",numTriggers)

                    if self.numTriggers > self.minPixelsChanged:
                        self.captureCount = 1 # capture ? sequences in a row

                if self.captureCount > 0:
                    print("Presence")
                    self.presence=1
                    self.captureCount = self.captureCount-1 
def main() :
    #while True:
    #USB=Maintenance_USB()
    #ARRET_USB=Redemarrage_post_maintenance(USB)
    try:
        Camera()
    except KeyboardInterrupt:
        exit()
    
if __name__ == "__main__":
    main()
    