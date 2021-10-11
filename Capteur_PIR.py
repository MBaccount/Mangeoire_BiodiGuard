#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Capteur_PIR
import RPi.GPIO as GPIO
import time

from ADCDevice import *

class Capteur_PIR :
    def __init__(self):
        self.adc= ADCDevice()
        if(self.adc.detectI2C(0x4b)): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found, \n"
                  "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
                  "Program Exit. \n");
            exit(-1)
        self.mouvement_en_cours=0
        self.presence=0
        time.sleep(1)

    def detection_de_mouvement(self) :
        if(self.adc.analogRead(1)==1) :
            mouvement=1 #Mouvement détecté
            #print("Il y a mouvement")
        else :
            mouvement=0
            #print("Il y a pas mouvement")
        
        return mouvement
    
    def gestion_dectetion(self):
        #Faire boucle# dans cette fonction en thread
        analyse=self.detection_de_mouvement() #Observe si il y a eu mouvement
        #print("Valeur d'analyse",analyse,"Voir self en cours",self.mouvement_en_cours)
        if(analyse!=self.mouvement_en_cours):
            #print("Il y a mouvement",analyse)
            #print(" ",)
            self.set_mouvement_en_cours(analyse)
            if(analyse==1):
                self.presence=1
            else:
                self.presence=0
        return self.presence
    
    def set_mouvement_en_cours(self,x):
        self.mouvement_en_cours=x
