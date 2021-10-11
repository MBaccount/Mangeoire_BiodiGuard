#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Barriere_IR
import RPi.GPIO as GPIO
from ADCDevice import *

class Barriere_IR :
    def __init__(self):
        self.adc=ADCDevice()
        if(self.adc.detectI2C(0x4b)): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found, \n"
                  "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
                  "Program Exit. \n");
            exit(-1)
    def recompense(self,ARRET_USB):
        Temps=0
        while Temps < 50 and ARRET_USB.stop_peripherique:
            Temps=Temps+1
            return self.adc.analogRead(2)
        
