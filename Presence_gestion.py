import io
import os
import time
import picamera
import numpy as np
from threading import Thread
import asyncio
import subprocess

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#threshold=30 # how much must the color value (0-255) change to be considered a change

class Presence_camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.width = 1440 # use lower resolution for motion check
        self.height = 1080
        self.minPixelsChanged = self.width * self.height * 2 / 100 # % change  # how many pixels must change to begin a save sequence
        print("minPixelsChanged=",self.minPixelsChanged) # debug
        print ('Creating in-memory stream')
        self.threshold=30 # how much must the color value (0-255) change to be considered a change
        self.stream = io.BytesIO()
        self.step = 1  # use this to toggle where the image gets saved
        self.numImages = 1 # count number of images processed
        self.captureCount = 0 # flag used to begin a sequence capture
        self.camera=picamera.PiCamera()
        self.data1=0
        self.data2=0
        self.data3=0
        self.presence=0
        self.camera.resolution = (1904,1088) #Il y a des meilleurs résultats avec une résolution élevé attention à ne pas excéder celle de la camera 
        #self.camera.resolution = (1440,1080)
        self.start()
        
    def get_presence(self):
        return self.presence
        
    def run(self):      
        while self.threshold > 0:
            try:
                self.presence=0
                #print ('Capture ' , self.numImages)
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
            except KeyboardInterrupt:
                break

    
    
class Presence_affichage(Thread):
    def __init__(self,Presence_camera):
        Thread.__init__(self)
        self.daemon = True
        self.Presence_camera=Presence_camera
        self.start()
        
    def run(self):
        while True:
            print("Valeur de la présence",self.Presence_camera.presence)
 
""" 
a=Presence_camera()
Presence_affichage(a)
"""
