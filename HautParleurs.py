#! /usr/bin/env python3
# coding: utf-8
# Création de la classe HautParleurs
import pygame #Librairie pour utiliser de la music
import datetime 
class HautParleurs :
    def __init__(self):
        self.heure_debut_musique=0
        self.nom_musique=''
        pygame.mixer.init()
        #self.pygame=pygame.mixer.init()
        
    def charger_musique(self,nomavecextension) :
        pygame.mixer.music.load("/home/pi/Music/"+nomavecextension)
        self.nom_musique=nomavecextension
    
    def jouer_musique(self):
        pygame.mixer.music.play()
        self.heure_debut_musique=datetime.datetime.now()
    
    def arret_en_ms(self,temps):
        pygame.mixer.music.fadeout(temps)
    
    def arret(self):
        pygame.mixer.music.stop()
        
    def set_volume(self,val):
        if (val>=0 and val<=100):
            vol=val/100
            if(vol>0.9):
                vol=vol-(vol-0.9)
        pygame.mixer.music.set_volume(vol)
    
    def get_volume(self):
        print("Le volume est",pygame.mixer.music.get_volume()*100,"%")
    
    def get_infos(self):
        return self.nom_musique, self.heure_debut_musique
        