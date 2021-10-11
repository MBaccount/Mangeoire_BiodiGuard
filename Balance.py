#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Balance
import RPi.GPIO as GPIO
from hx711 import HX711
import time
import math

from ADCDevice import *

class Balance :
    def __init__(self):
        self.hx = HX711()
        self.hx.set_reference_unit(569.6738)
        self.hx.reset()
        self.hx.tare()
        time.sleep(1)
        #print("Tare done! Add weight now... Init succed")
    
    def get_weight(self):
        val_en_g=self.hx.get_weight(5)
        val_en_g=round(val_en_g,1)
        if(val_en_g<0):
            val_en_g=0
        print("Le poids est de ",val_en_g," grammes")
        #self.hx.power_down()
        #self.hx.power_up()
        time.sleep(0.6)
        return val_en_g