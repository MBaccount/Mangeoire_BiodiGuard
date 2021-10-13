#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Leds
import RPi.GPIO as GPIO
import time
import datetime
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Leds :
    def __init__(self):
        #leds sous formes de tableau tel que (tab pour tableau): tab[led[tab[gpio_r,gpio_v,gpio_b],tab[couleur_r,couleur_v,couleur_b]]]
        self.leds=([[22,5,6],[0,0,0]],[[23,25,7],[0,0,0]],[[13,19,26],[0,0,0]],[[16,20,21],[0,0,0]])
        for i in range(4):
            for j in range(3):
                GPIO.setup(self.leds[i][0][j],GPIO.OUT)
        self.led1r=GPIO.PWM(self.leds[0][0][0],50)
        self.led1g=GPIO.PWM(self.leds[0][0][1],50)
        self.led1b=GPIO.PWM(self.leds[0][0][2],50)
        self.led2r=GPIO.PWM(self.leds[1][0][0],50)
        self.led2g=GPIO.PWM(self.leds[1][0][1],50)
        self.led2b=GPIO.PWM(self.leds[1][0][2],50)
        self.led3r=GPIO.PWM(self.leds[2][0][0],50)
        self.led3g=GPIO.PWM(self.leds[2][0][1],50)
        self.led3b=GPIO.PWM(self.leds[2][0][2],50)
        self.led4r=GPIO.PWM(self.leds[3][0][0],50)
        self.led4g=GPIO.PWM(self.leds[3][0][1],50)
        self.led4b=GPIO.PWM(self.leds[3][0][2],50)
       #---------------------------------------#
        self.led1r.start(0)
        self.led1g.start(0)
        self.led1b.start(0)
        self.led2r.start(0)
        self.led2g.start(0)
        self.led2b.start(0)
        self.led3r.start(0)
        self.led3g.start(0)
        self.led3b.start(0)
        self.led4r.start(0)
        self.led4g.start(0)
        self.led4b.start(0)
       #---------------------------------------#
       #Faire variable etat led pour allumé ou éteinte#
        self.pattern_current=0 #Variable du pattern en cours montré par la mangeoire
        self.option_current=0 #Variable de l'option en cours montré par la mangeoire modifier dans led pattern
        self.pattern_compulsory=0 #Variable qui indique quelle type de motif (pattern de stimuli) qui a été choisi
        self.option_compulsory=0 #Modifier option par self.option
        self.scenario=0#Variable qui indique dans quelle scénario on est
        self.random=0
        self.valr_commune=0
        self.valg_commune=0
        self.valb_commune=0
        self.L_or_R='Undefined'
        self.T_or_B='Undefined'
        self.One=0
        self.rotation=0
        self.horaire_delai=datetime.timedelta(hours=0, minutes=0,seconds=0)
        self.horaire_ouverture=datetime.timedelta(hours=0, minutes=0,seconds=0)
        self.horaire_fermeture=datetime.timedelta(hours=0, minutes=0,seconds=0)
        self.horaire_passe=datetime.timedelta(hours=0, minutes=0,seconds=0)
        self.led1r_scenario_5=0
        self.led1g_scenario_5=0
        self.led1b_scenario_5=0
        self.led2r_scenario_5=0
        self.led2g_scenario_5=0
        self.led2b_scenario_5=0
        self.C=0
        self.phase=0
        self.jour_ecoule=0
        self.allumage_du_jour=0
        self.motif_pattern="0000"
 

    def get_value_color_led(self,idled):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        rouge=self.leds[idled-1][1][0]
        vert=self.leds[idled-1][1][1]
        bleu=self.leds[idled-1][1][2]
        return rouge,vert,bleu

    def set_value_color_led(self,idled,val_r,val_v,val_b):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        if(not((val_r>=0 and val_r<=255 ) and (val_v>=0 and val_v<=255 ) and (val_b>=0 and val_b<=255 ))):
            return False
        self.leds[idled-1][1][0]=val_r
        self.leds[idled-1][1][1]=val_v
        self.leds[idled-1][1][2]=val_b
    
    def set_value_color_commun_led(self,val_r,val_v,val_b):
        if(not((val_r>=0 and val_r<=255 ) and (val_v>=0 and val_v<=255 ) and (val_b>=0 and val_b<=255 ))):
            return False
        for i in range(1,5):
            self.set_value_color_led(i,val_r,val_v,val_b)
        self.valr_commune=val_r
        self.valg_commune=val_v
        self.valb_commune=val_b
        
    
    def get_value_gpio_led(self,idled):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        gpio_rouge=self.leds[idled-1][0][0]
        gpio_vert=self.leds[idled-1][0][1]
        gpio_bleu=self.leds[idled-1][0][2]
        return gpio_rouge,gpio_vert,gpio_bleu

    def set_value_gpio_led(self,idled,val_gpio_r,val_gpio_v,val_gpio_b):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        self.leds[idled-1][0][0]=val_gpio_r
        self.leds[idled-1][0][1]=val_gpio_v
        self.leds[idled-1][0][2]=val_gpio_b
    
    def init_leds(self):
        self.led1r.start(0)
        self.led1g.start(0)
        self.led1b.start(0)
        self.led2r.start(0)
        self.led2g.start(0)
        self.led2b.start(0)
        self.led3r.start(0)
        self.led3g.start(0)
        self.led3b.start(0)
        self.led4r.start(0)
        self.led4g.start(0)
        self.led4b.start(0)
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        self.horaire_passe=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
       
    def conv_couleur_duty(self,valrgb):
        couleur_duty_cycle=(100.0/255.0)*valrgb
        return couleur_duty_cycle
    
    def allumage_leds(self,idled):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        if(idled==1):
            self.led1r.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][0]))
            self.led1g.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][1]))
            self.led1b.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][2]))
        if(idled==2):
            self.led2r.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][0]))
            self.led2g.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][1]))
            self.led2b.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][2]))
        if(idled==3):
            self.led3r.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][0]))
            self.led3g.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][1]))
            self.led3b.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][2]))
        if(idled==4):
            self.led4r.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][0]))
            self.led4g.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][1]))
            self.led4b.ChangeDutyCycle(self.conv_couleur_duty(self.leds[idled-1][1][2]))
            

    def extinction_leds(self,idled):
        if(idled!=1 and idled!=2 and idled!=3 and idled!=4):
            return False
        if(idled==1):
            #GPIO.cleanup()
            self.led1r.ChangeDutyCycle(0)
            self.led1g.ChangeDutyCycle(0)
            self.led1b.ChangeDutyCycle(0)
        elif(idled==2):
            self.led2r.ChangeDutyCycle(0)
            self.led2g.ChangeDutyCycle(0)
            self.led2b.ChangeDutyCycle(0)
        elif(idled==3):
            self.led3r.ChangeDutyCycle(0)
            self.led3g.ChangeDutyCycle(0)
            self.led3b.ChangeDutyCycle(0)
        elif(idled==4):
            self.led4r.ChangeDutyCycle(0)
            self.led4g.ChangeDutyCycle(0)
            self.led4b.ChangeDutyCycle(0)

    def leds_pattern0(self): #rajouter un paramètre pour prendre l'option_current
        self.pattern_current=0
        #activer l'allumage des leds
        if(self.option_current==0):
            self.allumage_leds(1)
            self.allumage_leds(2)
            self.allumage_leds(3)
            self.allumage_leds(4)
        elif(self.option_current==1):
            val_r=random.randint(0,255)
            val_v=random.randint(0,255)
            val_b=random.randint(0,255)
            self.set_value_color_commun_led(val_r,val_v,val_b)
            self.allumage_leds(1)
            self.allumage_leds(2)
            self.allumage_leds(3)
            self.allumage_leds(4)
        else:
            return False
            #ECRIRE DANS ALLUMAGE LEDS un renvoie à l'état de la LEDS
    
    def leds_pattern1(self):
        self.pattern_current=1
        if(self.option_current==0): #Les leds gauches sont allumées
            self.L_or_R='L'
            self.allumage_leds(1)
            self.allumage_leds(3) 
            self.extinction_leds(2)
            self.extinction_leds(4)
        elif(self.option_current==1):#Les leds droites sont allumées
            self.L_or_R='R'
            self.allumage_leds(2)
            self.allumage_leds(4) 
            self.extinction_leds(1)
            self.extinction_leds(3)
        elif(self.option_current==2):
            n=random.randint(0,1)
            val=['L','R']
            self.L_or_R=val[n] # Choisi aléatoirement L_or_R
            if(self.L_or_R=='L'): #Si L est choisi les leds de gauches sont allumées 
                self.allumage_leds(1)
                self.allumage_leds(3) 
                self.extinction_leds(2)
                self.extinction_leds(4)
            else: #Sinon les leds de droites sont allumées
                self.allumage_leds(2)
                self.allumage_leds(4) 
                self.extinction_leds(1)
                self.extinction_leds(3) 
        else:
            return False
        #print("Le self.L_or_R en cours",self.L_or_R)
    
    def leds_pattern2(self):
        self.pattern_current=2
        if(self.option_current==0): #Les leds du hauts sont allumées et ceux du bas éteintes
            self.T_or_B='T'
            self.allumage_leds(1)
            self.allumage_leds(2) 
            self.extinction_leds(3)
            self.extinction_leds(4) 
        elif(self.option_current==1):#Les leds du bas sont allumées et ceux du hauts sont éteintes
            self.T_or_B='B'
            self.allumage_leds(3)
            self.allumage_leds(4) 
            self.extinction_leds(1)
            self.extinction_leds(2)
        elif(self.option_current==2):
            n=random.randint(0,1) 
            val=['T','B']
            self.T_or_B=val[n] # Choisi aléatoirement T_or_B
            if(self.T_or_B=='T'):# Si T est choisi les leds du hauts sont allumées sinon c'est celles du bas 
                self.allumage_leds(1)
                self.allumage_leds(2) 
                self.extinction_leds(3)
                self.extinction_leds(4) 
            else:
                self.allumage_leds(3)
                self.allumage_leds(4) 
                self.extinction_leds(1)
                self.extinction_leds(2)
        else:
            return False
        #print("Le self.T_or_B en cours",self.T_or_B)
    
    def leds_pattern3(self): #Rajouter de quoi modifier one
        self.pattern_current=3
        if(self.option_current==0): #Si l'option 0 est choisi que la Led numéro 1 est choisi
            self.allumage_leds(1)
            self.extinction_leds(2) 
            self.extinction_leds(3)
            self.extinction_leds(4) 
        elif(self.option_current==1):
            if(self.One== 1 or self.One== 2 or self.One== 3 or self.One== 4):
                if(self.One!= 1) :
                    self.extinction_leds(1) 
                if(self.One!= 2) :
                    self.extinction_leds(2)
                if(self.One!= 3) :
                    self.extinction_leds(3)
                if(self.One!= 4) :
                    self.extinction_leds(4) 
                self.allumage_leds(self.One)
        elif(self.option_current==2):
            self.One=random.randint(1,4) #On peut indiquer qu'on choisi aléatoirement que si self.One n'est pas fixé
            if(self.One== 1 or self.One== 2 or self.One== 3 or self.One== 4):
                if(self.One!= 1) :
                    self.extinction_leds(1) 
                if(self.One!= 2) :
                    self.extinction_leds(2)
                if(self.One!= 3) :
                    self.extinction_leds(3)
                if(self.One!= 4) :
                    self.extinction_leds(4) 
                self.allumage_leds(self.One)
        else:
            return False
        
    def gestion_stimuli_led(self,valr,valg,valb,L_or_R,T_or_B,One):
        if(self.scenario==3):
            if(self.pattern_compulsory==0):#pattern_oiseaux=option en cours #Modifier la fonction allumage pour quantifier quand une led l'est
                if(self.option_compulsory==0):
                    if (self.pattern_compulsory==self.pattern_current and self.option_compulsory==self.option_current):
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
                elif(self.option_compulsory==1):
                    if (valr==self.valr_commune and valg==self.valg_commune and valb==self.valb_commune):
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
            if(self.pattern_compulsory==1):#patter_oiseaux=option en cours #Modifier la fonction allumage pour quantifier quand une led l'est
                if(self.option_compulsory==0 or self.option_compulsory==1):
                    if (self.pattern_compulsory==self.pattern_current and self.option_compulsory==self.option_current):
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
                elif(self.option_compulsory==2):
                    if (self.L_or_R==L_or_R): #Affecter une valeur à L_or_R
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
            if(self.pattern_compulsory==2):#patter_oiseaux=option en cours #Modifier la fonction allumage pour quantifier quand une led l'est
                if(self.option_compulsory==0 or self.option_compulsory==1):
                    if (self.pattern_compulsory==self.pattern_current and self.option_compulsory==self.option_current):
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
                elif(self.option_compulsory==2):
                    if (self.T_or_B==T_or_B): #Affecter une valeur à T_or_B
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
            if(self.pattern_compulsory==3):#patter_oiseaux=option en cours #Modifier la fonction allumage pour quantifier quand une led l'est
                if(self.option_compulsory==0 or self.option_compulsory==1):
                    if (self.pattern_compulsory==self.pattern_current and self.option_compulsory==self.option_current):
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
                elif(self.option_compulsory==2):
                    if (self.One==One): #Affecter une valeur à la led qui doit s'allumer
                        return 1 #Pour oiseaux autorisé
                    else:
                        return 0 #Pour oiseaux non autorisé
            
    def set_random(self,x):
        self.random=x
    def set_pattern_current(self,x):
        self.pattern_current=x
    def get_pattern_current(self):
        return self.pattern_current 
    def set_option_current(self,x):
        self.option_current=x
    def get_option_current(self):
        return self.option_current
    def set_pattern_compulsory(self,x):
        self.pattern_compulsory=x
    def get_pattern_compulsory(self):
        return self.pattern_compulsory
    def set_option_compulsory(self,x):
        self.option_compulsory=x
    def get_option_compulsory(self):
        return self.option_compulsory
    def set_scenario(self,x):
        self.scenario=x
    def get_scenario(self):
        return self.scenario
    def set_L_or_R(self,x):
        self.L_or_R=x
    def set_T_or_B(self,x):
        self.T_or_B=x
    def set_one(self,x):
        self.one=x
    def set_C(self,x):
        self.C=x
    def get_C(self):
        return self.C  
    def set_phase(self,x):
        self.phase=x
    def get_phase(self):
        return self.phase
    def set_leds1_scenario_5(self,led1r_scenario_5,led1g_scenario_5,led1b_scenario_5):
        self.led1r_scenario_5=led1r_scenario_5
        self.led1g_scenario_5=led1g_scenario_5
        self.led1b_scenario_5=led1b_scenario_5
    def set_leds2_scenario_5(self,led2r_scenario_5,led2g_scenario_5,led2b_scenario_5):
        self.led2r_scenario_5=led2r_scenario_5
        self.led2g_scenario_5=led2g_scenario_5
        self.led2b_scenario_5=led2b_scenario_5        
    def get_leds1_scenario_5(self):
        return self.led1r_scenario_5,self.led1g_scenario_5,self.led1b_scenario_5
    def get_leds2_scenario_5(self):
        return self.led2r_scenario_5,self.led2g_scenario_5,self.led2b_scenario_5    
    def set_horaire_ouverture(self,x):
        self.horaire_ouverture=x
    def get_horaire_ouverture(self):
        return self.horaire_ouverture
    def set_horaire_fermeture(self,x):
        self.horaire_fermeture=x
    def get_horaire_fermeture(self):
        return self.horaire_fermeture
    def set_horaire_delai(self,x):
        self.horaire_delai=datetime.timedelta(hours=0, minutes=0, seconds=x)
    def get_horaire_delai(self):
        return self.horaire_delai
    def get_leds_color_in_str(self):
        valr1,valv1,valb1=self.get_value_color_led(1)
        led1=[str(valr1),str(valv1),str(valb1)]
        valr2,valv2,valb2=self.get_value_color_led(2)
        led2=[str(valr2),str(valv2),str(valb2)]
        valr3,valv3,valb3=self.get_value_color_led(3)
        led3=[str(valr3),str(valv3),str(valb3)]
        valr4,valv4,valb4=self.get_value_color_led(4)
        led4=[str(valr4),str(valv4),str(valb4)]
        return led1,led2,led3,led4
    
    def get_pattern(self):
        if (self.pattern_current==0):
            self.motif_pattern='1111'
        if (self.pattern_current==1 and self.L_or_R=='L'):
            self.motif_pattern='1010'
        if (self.pattern_current==1 and self.L_or_R=='R'):
            self.motif_pattern='0101'
        if (self.pattern_current==2 and self.T_or_B=='T'):
            self.motif_pattern='1100'
        if (self.pattern_current==2 and self.T_or_B=='B'):
            self.motif_pattern='0011'
        if (self.pattern_current==3 and self.One==1 and self.option_current!=0 or self.pattern_current==3 and self.option_current==0):
            self.motif_pattern='1000'
        if (self.pattern_current==3 and self.One==2 and self.option_current!=0):
            self.motif_pattern='0100'
        if (self.pattern_current==3 and self.One==3 and self.option_current!=0):
            self.motif_pattern='0010'
        if (self.pattern_current==3 and self.One==4 and self.option_current!=0):
            self.motif_pattern='0001'

        return self.motif_pattern
    
    def variation_pattern(self):
        #print("Pattern:",self.pattern_current,"Option pattern",self.option_current)
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        seconds_actuelles=datetime.datetime.now().second
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles, seconds=seconds_actuelles)
        if(horaire_actuelle>=self.horaire_ouverture and horaire_actuelle<self.horaire_fermeture):
            if(self.random==0 and self.allumage_du_jour==0):
                print('Mode sans variation')
                self.allumage_du_jour=1
                self.option_current=self.option_compulsory#Le mieux serait de créer une alternance entre option 0 et 1
                if(self.pattern_compulsory==0):
                    self.leds_pattern0() 
                if(self.pattern_compulsory==1):
                    self.leds_pattern1()
                if(self.pattern_compulsory==2):
                    self.leds_pattern2()
                if(self.pattern_compulsory==3):
                    self.leds_pattern3()
                
            if(horaire_actuelle>=self.horaire_passe+self.horaire_delai and self.random==1):
                self.horaire_passe=horaire_actuelle
                self.pattern_current=random.randint(0,3)
                if(self.pattern_current==0):
                    self.option_current=random.randint(0,1)
                    self.leds_pattern0()
                    print("Mode variation: Pattern:",self.pattern_current,"Option pattern",self.option_current,"Motif du pattern allumé",self.get_pattern())
                else:
                    self.option_current=random.randint(0,2)
                    if(self.pattern_current==1):
                        self.leds_pattern1()
                    if(self.pattern_current==2):
                        self.leds_pattern2()
                    if(self.pattern_current==3):
                        self.leds_pattern3()
                    print("Mode variation: Pattern:",self.pattern_current,"Option pattern",self.option_current,"Motif du pattern allumé",self.get_pattern())
    def scenario_5(self): #Faire set_c et set_led_scenario5
        if(self.scenario==5):
            if(self.phase==1 or self.phase==3):
                if(self.C==0): #Traiter les jours restants dans config
                    self.set_value_color_commun_led(self.led1r_scenario_5,self.led1g_scenario_5,self.led1b_scenario_5)
                    self.option_current=0
                    self.leds_pattern0()
                else:
                    self.set_value_color_commun_led(self.led2r_scenario_5,self.led2g_scenario_5,self.led2b_scenario_5)
                    self.option_current=0
                    self.leds_pattern0()
            if(self.phase==2):
                heures_actuelles=datetime.datetime.now().hour
                minutes_actuelles=datetime.datetime.now().minute
                seconds_actuelles=datetime.datetime.now().second
                horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles, seconds=seconds_actuelles)
                if(horaire_actuelle>=self.horaire_passe+self.horaire_delai):
                    self.horaire_passe=horaire_actuelle
                    if(self.C==0):
                        self.set_value_color_commun_led(self.led1r_scenario_5,self.led1g_scenario_5,self.led1b_scenario_5)
                        self.option_current=0
                        self.leds_pattern0()
                        self.C=1
                    else:
                        self.set_value_color_commun_led(self.led2r_scenario_5,self.led2g_scenario_5,self.led2b_scenario_5)
                        self.option_current=0
                        self.leds_pattern0()
                        self.C=0
                return self.horaire_passe

        
