#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Servomoteurs
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Servomoteurs :
    def __init__(self):
        #Les servomoteurs sous formes d'un tableau tel que (tab pour tableau): tab[servo[tab[gpio,pourcentage_ouverture,etat_d'activation,freq]]]
        self.servomoteurs=([12,0,0,50],[18,0,0,50])
        GPIO.setup(self.servomoteurs[0][0], GPIO.OUT)
        GPIO.setup(self.servomoteurs[1][0], GPIO.OUT)
        self.servo1=GPIO.PWM(self.servomoteurs[0][0], self.servomoteurs[0][3])
        self.servo2=GPIO.PWM(self.servomoteurs[1][0], self.servomoteurs[1][3])
        self.etat_porte=0
        self.date_du_jour=0
        self.date_debut=0
        self.delai=0
        self.probabilite_ouverture=0
        self.nombre_ouverture=0
        self.autorisation_ouverture=0
        self.horaire_ouverture=datetime.timedelta(hours=0, minutes=0)
        self.horaire_fermeture=datetime.timedelta(hours=0, minutes=0)
        self.scenario=0
        self.autorisation=0
        self.nom_of=''
        self.sans_punition=0

    def set_pourcentage_servo (self,idservo,pourcentage) :
        #Fonction qui sert à définir l'angle d'ouverture et le pourcentage d'ouverture de la porte complètement ou non comme dans le scénario 2
        if (pourcentage < 0 or pourcentage > 100 ):
            raise Exception("Le pourcentage n'est pas dans l'intervalle [0;100]")
        if(idservo!=1 and idservo!=2):
            return False
        self.servomoteurs[idservo-1][1]=pourcentage
        time.sleep(0.1)

   
    def get_gpio_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        else :
            return self.servomoteurs[idservo-1][0]
    
    def get_angle_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        else :
            return self.servomoteurs[idservo-1][1]

    def get_etat_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        else :
            return self.servomoteurs[idservo-1][2]
                 
    def get_freq_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        else :
            return self.servomoteurs[idservo-1][3]
        
    def init_servomoteur(self):
        self.servo1.start(1.1)
        time.sleep(0.6)
        self.servo1.ChangeDutyCycle(0)
        self.servo2.start(1.1)
        time.sleep(0.6)
        self.servo2.ChangeDutyCycle(0)
    
    def activation_servo(self,idservo):
        #print("activation_servo")
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        rapport = 1.1 +(11.7-1.1)*self.servomoteurs[idservo-1][1]/100.0
        #print("rapport :",rapport)
        if(idservo==1):
            self.servomoteurs[idservo-1][2]=1 #indique que le servomoteur 1 est activé
            self.servo1.ChangeDutyCycle(rapport)
            time.sleep(0.5)
            self.servo1.ChangeDutyCycle(1.1)
            time.sleep(0.5)
            self.servo1.ChangeDutyCycle(0)
            self.servomoteurs[idservo-1][2]=0
        elif(idservo==2):
            self.servomoteurs[idservo-1][2]=1 #indique que le servomoteur 2 est activé
            self.servo2.ChangeDutyCycle(rapport)
            time.sleep(0.6)
            self.servo2.ChangeDutyCycle(0)
            self.servomoteurs[idservo-1][2]=0
    
    def desactivation_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        if(idservo==1):
            self.servo1.ChangeDutyCycle(0)#
            self.servomoteurs[idservo-1][2]=0 #indique que le servomoteur 1 est désactivé
        elif(idservo==2):
            self.servo2.ChangeDutyCycle(0)#
            self.servomoteurs[idservo-1][2]=0 #indique que le servomoteur 2 est désactivé
    
    def arret_servo(self,idservo):
        if(idservo!=1 and idservo!=2):
            raise Exception("L'id du servomoteur spécifié ne correspond pas, choix possible 1 ou 2")
        if(idservo==1):
            self.servo1.ChangeDutyCycle(1.1)#Valeur position par défaut
            time.sleep(0.6)
            self.servo1.stop()#
            self.servomoteurs[idservo-1][2]=0 #indique que le servomoteur 1 est arreté
        elif(idservo==2):
            self.servo1.ChangeDutyCycle(1.1)#Valeur position par défaut
            time.sleep(0.6)
            self.servo2.stop()#
            self.servomoteurs[idservo-1][2]=0 #indique que le servomoteur 2 est arreté
      
    def activation_porte(self):
        idservo=2 #nourriture servo
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
        if(horaire_actuelle>=self.horaire_ouverture and horaire_actuelle<self.horaire_fermeture and self.etat_porte==0):
        #if(horaire_actuelle>=self.horaire_ouverture and horaire_actuelle<self.horaire_fermeture and self.autorisation==1 and self.etat_porte==0):
            self.activation_servo(idservo)
            self.etat_porte=1
        elif(horaire_actuelle>=self.horaire_fermeture and self.etat_porte==1):
            self.arret_servo(idservo)
                         
    def activation_nourriture(self,Nom_OF_Oiseau=''):
        idservo=1 #nourriture servo
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
        if(horaire_actuelle>=self.horaire_ouverture and horaire_actuelle<self.horaire_fermeture and self.autorisation==1 and self.etat_porte==1):
            if(self.sans_punition==0):
                #print("On est avec punition c'est-à-dire dans reward enable_recompense=1 et dans punishment without=1")
                if(self.scenario==2 or self.scenario==3 or self.scenario==4 or self.scenario==5): #Rajouter tous les scenarios dont l'ouverture de la porte est assez classique
                    self.activation_servo(idservo)
                if(self.scenario==6):
                    if(self.nom_of==Nom_OF_Oiseau):
                        self.activation_servo(idservo)
                if(self.scenario==7):#Pensé à considérer que si on a un retour négatif c'est que la date n'est pas arrivé on est donc en phase reference
                    print(self.jour_ecoule)
                    if(self.jour_ecoule<0):
                        self.activation_servo(idservo)
                    else:
                        self.probabilite_ouverture=self.probabilite_ouverture+1/pow(2,self.jour_ecoule+1)
                        print("Affichage de la probabilité du jour",self.probabilite_ouverture)
                        if(self.probabilite_ouverture==1):
                            self.probabilite_ouverture=0
                            self.activation_servo(idservo)
                if(self.scenario==8):
                    if(self.jour_ecoule<0):
                        self.activation_servo(idservo)
                    elif(self.nombre_ouverture<=self.nb_ouverture_autorise):
                        print("self.nombre d'ouverture autorisé")
                        self.nombre_ouverture=self.nombre_ouverture+1
                        self.activation_servo(idservo)
                if(self.scenario==9):
                    if(self.jour_ecoule<0):
                        self.activation_servo(idservo)
                    else:
                        self.delai=pow(2,self.jour_ecoule+1)
                        print("Affichage de la probabilité du jour",self.delai)
                        time.sleep(self.delai)
                        self.activation_servo(idservo)
            else:
                print("On n'est sans punition")
                self.activation_servo(idservo)

    def set_sans_punition(self,x):
        self.sans_punition=x
    def get_sans_punition(self):
        return self.sans_punition
    def set_horaire_ouverture(self,x):
        self.horaire_ouverture=x
    def get_horaire_ouverture(self):
        return self.horaire_ouverture
    def set_horaire_fermeture(self,x):
        self.horaire_fermeture=x
    def get_horaire_fermeture(self):
        return self.horaire_fermeture
    def set_scenario(self,x):
        self.scenario=x
    def get_scenario(self):
        return self.scenario
    def set_autorisation(self,x):
        self.autorisation=x
    def get_autorisation(self):
        return self.autorisation
    def set_nombre_ouverture(self,x):
        self.nombre_ouverture=x
    def get_nombre_ouverture(self):
        return self.nombre_ouverture
    def set_nb_ouverture_autorise(self,x):
        self.nb_ouverture_autorise=x
    def get_nb_ouverture_autorise(self):
        return self.nb_ouverture_autorise
    def set_delai(self,x):
        self.delai=x
    def get_jour_ecoule(self):
        return self.jour_ecoule
    def set_jour_ecoule(self,x):
        self.jour_ecoule=x
    def get_delai(self):
        return self.delai
    def get_etat_porte(self):
        return self.etat_porte
    def get_probabilite_ouverture(self):
        return self.probabilite_ouverture
    def verification_horaire_porte(self):
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
        if(horaire_actuelle >= self.horaire_ouverture and horaire_actuelle <= self.horaire_fermeture):
            return True
        else:
            return False
    def set_nom_of(self,x):
        self.nom_of=x
    def get_nom_of(self):
        return self.nom_of