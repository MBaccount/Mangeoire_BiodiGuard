#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Camera2
import time
import cv2
import datetime

class Camera2 :
    def __init__(self):
        self.camera=cv2.VideoCapture(1)
        if not(self.camera.isOpened()):
            self.camera=cv2.VideoCapture(0)
        self.camera.set(3, 1920)
        self.camera.set(4, 1080)
           
    def set_resolution(self,width, height):
        self.camera.set(3, width)
        self.camera.set(4, height)
       
    def photo (self,individu) :
        ret, image=self.camera.read()
        date_time=datetime.datetime.now()
        name= date_time.strftime("%m_%d_%Y__%H_%M_%S")
        if ret:
            cv2.imwrite('/home/pi/Desktop/Images/camera2'+name+individu+'.jpg',image)
        
    def film (self,individu):
        """
        A modifier
        """
        date_time=datetime.datetime.now()
        name= date_time.strftime("%m_%d_%Y__%H_%M_%S")
        """
        self.camera.start_recording('/home/pi/Desktop/camera2'+name+individu+'.h264')
        time.sleep(5)
        self.camera.stop_recording()
        """
    def free(self):
        self.camera.release()