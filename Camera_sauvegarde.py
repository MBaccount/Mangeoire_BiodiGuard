#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Camera
import time
import datetime
from picamera import PiCamera

class Camera :
    def __init__(self):
        self.camera=PiCamera()
       
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
        
    