#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Witty Pi
import time
import datetime

import subprocess

class Witty_Pi :
    def __init__(self):
        self.horaire_allumage=datetime.timedelta(hours=0, minutes=0)
        self.horaire_extinction=datetime.timedelta(hours=0, minutes=0)
        self.horaire_transmission=datetime.timedelta(hours=0, minutes=0)
        
    def creation_schedule(self):
        date_today=datetime.date.today().strftime('%Y-%m-%d')
        delta_journee=datetime.timedelta(hours=23, minutes=59)
        delta_allumage=self.horaire_extinction-self.horaire_allumage
        delta_extinction=delta_journee-delta_allumage
        
        secs_debut = self.horaire_allumage.total_seconds()
        horaire_debut_voulue_hour = str(int(secs_debut / 3600))
        horaire_debut_voulue_minute= str(int(secs_debut / 60) % 60)
        
        secs_fin = self.horaire_extinction.total_seconds()
        horaire_fin_voulue_hour = str(int(secs_fin / 3600))
        horaire_fin_voulue_minute= str(int(secs_fin / 60) % 60)
        
        secs_debut = delta_allumage.total_seconds()
        delta_allumage_hour= str(int(secs_debut / 3600))
        delta_allumage_minute= str(int(secs_debut / 60) % 60)
        
        secs_fin = delta_extinction.total_seconds()
        delta_extinction_hour= int(secs_fin / 3600)
        delta_extinction_minute= int(secs_fin / 60) % 60
        
        if(delta_extinction_minute==59):
            delta_extinction_hour=delta_extinction_hour+1
            delta_extinction_minute=00
        else:
            delta_extinction_minute=delta_extinction_minute+1
            
        delta_extinction_hour=str(delta_extinction_hour)
        delta_extinction_minute=str(delta_extinction_minute)
        
        fichier = open("/home/pi/wittypi/schedule.wpi", "w") #Rajouter si minute ou heure <10 rajouter des 0
        if(int(horaire_debut_voulue_hour)<10 and int(horaire_debut_voulue_minute)>=10):
            fichier.write("BEGIN "+date_today+' '+'0'+horaire_debut_voulue_hour+':'+horaire_debut_voulue_minute+':'+"00")
        if(int(horaire_debut_voulue_hour)>=10 and int(horaire_debut_voulue_minute)<10):
            fichier.write("BEGIN "+date_today+' '+horaire_debut_voulue_hour+':'+'0'+horaire_debut_voulue_minute+':'+"00")
        if(int(horaire_debut_voulue_hour)<10 and int(horaire_debut_voulue_minute)<10):
            fichier.write("BEGIN "+date_today+' '+'0'+horaire_debut_voulue_hour+':'+'0'+horaire_debut_voulue_minute+':'+"00")
        if(int(horaire_debut_voulue_hour)>=10 and int(horaire_debut_voulue_minute)>=10):
            fichier.write("BEGIN "+date_today+' '+horaire_debut_voulue_hour+':'+horaire_debut_voulue_minute+':'+"00")       
        if(int(horaire_fin_voulue_hour)<10 and int(horaire_fin_voulue_minute)>=10):
            fichier.write("\nEND   "+date_today+' '+'0'+horaire_fin_voulue_hour+':'+horaire_fin_voulue_minute+':'+"00")
        if(int(horaire_fin_voulue_hour)<10 and int(horaire_fin_voulue_minute)>=10):
            fichier.write("\nEND   "+date_today+' '+horaire_fin_voulue_hour+':'+'0'+horaire_fin_voulue_minute+':'+"00")
        if(int(horaire_fin_voulue_hour)<10 and int(horaire_fin_voulue_minute)<10):
            fichier.write("\nEND   "+date_today+' '+'0'+horaire_fin_voulue_hour+':'+'0'+horaire_fin_voulue_minute+':'+"00")
        if(int(horaire_fin_voulue_hour)>=10 and int(horaire_fin_voulue_minute)>=10):
            fichier.write("\nEND   "+date_today+' '+horaire_fin_voulue_hour+':'+horaire_fin_voulue_minute+':'+"00")
        
        fichier.write("\nON   "+' H'+delta_allumage_hour+' M'+delta_allumage_minute)
        fichier.write("\nOFF  "+' H'+delta_extinction_hour+' M'+delta_extinction_minute+"\n")
        
        """    
        if(int(delta_allumage_hour)>10):
            fichier.write("\nON   "+' H'+delta_allumage_hour+' M'+delta_allumage_minute)
        if(int(delta_allumage_hour)<10):
            fichier.write("\nON   "+' H'+delta_allumage_hour+'  M'+delta_allumage_minute)
        if(int(delta_extinction_hour)>10):
            fichier.write("\nOFF  "+' H'+delta_extinction_hour+' M'+delta_extinction_minute+"\n")
        if(int(delta_extinction_hour)<10):
            fichier.write("\nOFF  "+' H'+delta_extinction_hour+'  M'+delta_extinction_minute+"\n")
         """   
        
        fichier.close()
        
        
        #A décommenter l'inscription suivante qui permet l'execution de script du wittypi pour l'extinction
        #subprocess.call(["bash","-c","source ~/.profile; "+'sudo /home/pi/wittypi/runScript.sh'])
                
    def verification_horaire_systeme(self):
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
        if(horaire_actuelle >= self.horaire_allumage and horaire_actuelle <= self.horaire_transmission):
            return True
        else:
            return False
        
        
    def set_horaire(self,horaire_allumage,horaire_extinction,horaire_transmission):
        self.horaire_allumage=horaire_allumage
        self.horaire_extinction=horaire_extinction
        self.horaire_transmission=horaire_transmission