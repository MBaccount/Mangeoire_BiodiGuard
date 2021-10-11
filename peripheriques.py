#! /usr/bin/env python3
# coding: utf-8
# Test des classes des périphériques
import time
import datetime
import RPi.GPIO as GPIO
import subprocess

import threading
import sys
from Barriere_IR import Barriere_IR
#from Balance import Balance
from Camera import Camera
from Camera2 import Camera2
from Capteur_PIR import Capteur_PIR
from Capteur_RFID import Capteur_RFID
from Compteur import Compteur
from Config import Config
from Enregistrement import Enregistrement
from HautParleurs import HautParleurs
from Leds import Leds
from Servomoteurs import Servomoteurs
from Witty_Pi import Witty_Pi
from try_thread_usb_detect import Maintenance_USB,Redemarrage_post_maintenance



def init_peripheriques():
    #BALANCE=Balance()
    BARRIERE_IR=Barriere_IR()
    CAMERA=Camera()
    CAMERA2=Camera2()
    COMPTEUR=Compteur()
    CONFIGURATION=Config()
    CAPTEUR_PIR=Capteur_PIR()
    ENREGISTREMENT=Enregistrement()
    HAUT_PARLEURS=HautParleurs()
    LEDS=Leds()
    RFID=Capteur_RFID()
    SERVOMOTEURS=Servomoteurs()
    WITTYPI=Witty_Pi()
    
    return RFID,BARRIERE_IR,CAMERA,CAMERA2,CAPTEUR_PIR,HAUT_PARLEURS,CONFIGURATION,ENREGISTREMENT,LEDS,COMPTEUR,SERVOMOTEURS,WITTYPI
    #return RFID,BARRIERE_IR,CAMERA2,CAPTEUR_PIR,HAUT_PARLEURS,CONFIGURATION,ENREGISTREMENT,LEDS,COMPTEUR,SERVOMOTEURS,WITTYPI

    #return RFID,BALANCE,BARRIERE_IR,CAMERA,CAMERA2,CAPTEUR_PIR,HAUT_PARLEURS,CONFIGURATION,ENREGISTREMENT,LEDS,COMPTEUR,SERVOMOTEURS,WITTYPI
    
def affectation_config(RFID,LEDS,CONFIGURATION,SERVOMOTEURS,WITTYPI):
    scenario, nom, emplacement_of, autorisation_recompense, probabilite_recompense,sans_punition=CONFIGURATION.renvoie_config_general()
    horaire_allumage,horaire_extinction,horaire_ouverture_porte,horaire_fermeture_porte,horaire_allumage_leds,horaire_extinction_leds,delai_leds,delai_punition,jour_ecoule,horaire_transmission=CONFIGURATION.renvoie_config_horaire()
    pattern,option_pattern,L_or_R,T_or_B,one,random,with_all,c,j,phase=CONFIGURATION.renvoie_config_leds()
    ledr1,ledv1,ledb1,ledr2,ledv2,ledb2,ledr3,ledv3,ledb3,ledr4,ledv4,ledb4,ledrall,ledvall,ledball=CONFIGURATION.renvoie_couleurs_leds()
    facteur_division, portion_de_debut, phase_rfid, duree_par_portion=CONFIGURATION.renvoie_config_pittags()
    pourcentage_open_position, poucentage_close_position, pourcentage_ouverture_nourriture=CONFIGURATION.renvoie_config_servomoteurs()
    
    CONFIGURATION.verification_dossier_images()
 
    LEDS.set_horaire_ouverture(horaire_allumage_leds)
    LEDS.set_horaire_fermeture(horaire_extinction_leds)
    LEDS.set_scenario(scenario)
    LEDS.set_random(random) #Rajouter random
    LEDS.set_pattern_compulsory(pattern)
    LEDS.set_option_compulsory(option_pattern)
    LEDS.set_L_or_R(L_or_R)
    LEDS.set_T_or_B(T_or_B)
    LEDS.set_one(one)
    #print("with_all",with_all)
    if(with_all==0):
        LEDS.set_value_color_led(1,ledr1,ledv1,ledb1)
        LEDS.set_value_color_led(2,ledr2,ledv2,ledb2)
        LEDS.set_value_color_led(3,ledr3,ledv3,ledb3)
        LEDS.set_value_color_led(4,ledr4,ledv4,ledb4)
    else:
        LEDS.set_value_color_commun_led(ledrall,ledvall,ledball)
    ###Mettre dans la suite dans une fonction de LEDS, ajouter une non variation de la lumière dans ce mode
        
    if(scenario==5):
        CONFIGURATION.modifier_config_scenario_5()
        LEDS.set_C(c)
        LEDS.set_phase(phase)
        LEDS.set_leds1_scenario_5(ledr1,ledv1,ledb1)
        LEDS.set_leds2_scenario_5(ledr2,ledv2,ledb2)
        RFID.set_phase(phase)

    if(scenario==6):
        RFID.init_scenario_6()
        RFID.set_nom_OF(nom)
        RFID.set_phase(phase_rfid)
        SERVOMOTEURS.set_nom_of(nom)


    LEDS.set_horaire_delai(delai_leds)
    led1,led2,led3,led4=LEDS.get_leds_color_in_str()
    
    RFID.set_pittag_choices(facteur_division, portion_de_debut,duree_par_portion)
    
    SERVOMOTEURS.set_pourcentage_servo(2,pourcentage_open_position) #Indique pourcentage ouverture porte
    SERVOMOTEURS.set_pourcentage_servo(1,pourcentage_ouverture_nourriture) #Indique pourcentage ouverture nourriture
    SERVOMOTEURS.set_horaire_ouverture(horaire_ouverture_porte)
    SERVOMOTEURS.set_horaire_fermeture(horaire_fermeture_porte)
    SERVOMOTEURS.set_autorisation(autorisation_recompense) #Permet la prise en compte de laccès au servomoteur nourriture
    SERVOMOTEURS.set_jour_ecoule(jour_ecoule)
    SERVOMOTEURS.set_scenario(scenario)
    SERVOMOTEURS.set_delai(delai_punition)
    SERVOMOTEURS.set_sans_punition(sans_punition)
    SERVOMOTEURS.init_servomoteur()
    WITTYPI.set_horaire(horaire_allumage,horaire_extinction,horaire_transmission)
    WITTYPI.creation_schedule()
    
    date_time=datetime.datetime.now()
    jour= date_time.strftime("%d_%m_%Y")
    
    
    return jour,scenario, nom, emplacement_of,pattern,option_pattern,led1,led2,led3,led4
    

def run_again(cmd):
    subprocess.call(["bash","-c","source ~/.profile; "+cmd])

def traitement_scenario(ARRET_USB,USB):
    #Création des objets périphériques
    #RFID,BARRIERE_IR,CAMERA2,CAPTEUR_PIR,HAUT_PARLEURS,CONFIGURATION,ENREGISTREMENT,LEDS,COMPTEUR,SERVOMOTEURS,WITTYPI=init_peripheriques()
    RFID,BARRIERE_IR,CAMERA,CAMERA2,CAPTEUR_PIR,HAUT_PARLEURS,CONFIGURATION,ENREGISTREMENT,LEDS,COMPTEUR,SERVOMOTEURS,WITTYPI=init_peripheriques()
    #Affectation des configurations du CONFIG.INI au périphérique et renvoie des configurations générales
    jour,scenario, nom_of, emplacement_of,pattern,option_pattern,led1,led2,led3,led4=affectation_config(RFID,LEDS,CONFIGURATION,SERVOMOTEURS,WITTYPI)  
    
    while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
        ######
        ######
        #Faire exécution parallèle d'action et d'observation
        ######
        ######

        if(scenario<1):
            #send error to Xbee
            raise Exception("Scénario inférieur à 1,veuillez entrer un scénario compris entre [1-9]")
            
        if(scenario==1):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    if(CAMERA.get_presence()==1):
                    #if(True):
                        print("Une présence a été détecté")
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        recompense=BARRIERE_IR.recompense(ARRET_USB)
                        #Rajouter l'option pattern et le pattern aussi dans l'app de config et dans enregistrement
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,"Scénario sans Pittag",1,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)

        if(scenario==2):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    if(CAMERA.get_presence()==1):
                    #if(True):
                        print("Une présence a été détecté")
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        SERVOMOTEURS.activation_nourriture()
                        recompense=BARRIERE_IR.recompense(ARRET_USB)
                        print("Recompense",recompense)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,"Scénario sans Pittag",1,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==3):
            while(WITTYPI.verification_horaire_systeme()and ARRET_USB.stop_peripherique):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    #a=CAPTEUR_PIR.gestion_dectetion()
                    #b=CAMERA.get_presence()
                    if(CAMERA.get_presence()==1):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(True):
                        print("Une présence a été détecté")
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()  
                        autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau=RFID.pittags_gestionnaire(scenario,ARRET_USB)
                        if(autorisation==1):
                            print("Résultat de la RFID autorisation [",autorisation,"],pittag[",pittag,"]")
                            autorisation=0
                            autorisation=LEDS.gestion_stimuli_led(valr,valg,valb,L_or_R,T_or_B,One)
                            #print("autorisation",autorisation)
                            print("Résultat de l'autorisation via le bon stimuli visuel [",autorisation,"],pittag[",pittag,"]")
                            if(autorisation==1):
                                print("L'oiseau est venu au bon pattern")
                                SERVOMOTEURS.activation_nourriture()
                                recompense=BARRIERE_IR.recompense(ARRET_USB)   
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,"Scénario sans Pittag",autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                       
                        
        if(scenario==4):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    RFID.variation_temporelle()
                    if(CAMERA.get_presence()==1):
                    #if(True):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        autorisation,pittag=RFID.pittags_gestionnaire(scenario,ARRET_USB)
                        print("Résultat de la RFID autorisation [",autorisation,"],pittag[",pittag,"]")
                        if(autorisation==1):
                            print("Fait partie de la bonne partie de liste")
                            SERVOMOTEURS.activation_nourriture()
                            recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,pittag,autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==5):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    if(LEDS.get_phase==2):
                        RFID.set_horaire_init(LEDS.scenario_5())
                    else:
                        LEDS.scenario_5()
                    #if(True):
                    if(CAMERA.get_presence()==1):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        autorisation,pittag=RFID.pittags_gestionnaire(scenario,ARRET_USB) #DOnner l'heure de la variation de la led et ajouter la variation led pour ce scénario
                        print("Résultat de la RFID autorisation [",autorisation,"],pittag[",pittag,"]")
                        if(autorisation==1):
                            SERVOMOTEURS.activation_nourriture()
                            recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,pittag,autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==6):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    #if(True):
                    if(CAMERA.get_presence()==1):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                        print("Presence détecté")
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        autorisation,pittag=RFID.pittags_gestionnaire(scenario,ARRET_USB)
                        print("Résultat de la RFID autorisation [",autorisation,"],pittag[",pittag,"]")
                        if(autorisation==1):
                            SERVOMOTEURS.activation_nourriture()
                            recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,pittag,autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==7):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                autorisation=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    if(CAMERA.get_presence()==1):
                    #if(True):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        #print("Cam 1 fini")
                        CAMERA2.photo(str(nbr_individu))
                        #print("Cam 2 fini")
                        #poids=BALANCE.get_weight()
                        if(SERVOMOTEURS.get_sans_punition()==0):
                            print("Présence détecté")
                            SERVOMOTEURS.activation_nourriture()
                            if(SERVOMOTEURS.get_probabilite_ouverture()==0):#Voir programme la probabilité passe à 1 puis 0 jusqu'à nouvelle activation du servomoteur
                                autorisation=1
                                recompense=BARRIERE_IR.recompense(ARRET_USB)
                        else:
                            autorisation=1
                            SERVOMOTEURS.activation_nourriture()
                            recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,"Scénario sans Pittag",autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==8):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    #if(True):
                    if(CAMERA.get_presence()==1):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):   
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        autorisation,pittag=RFID.pittags_gestionnaire(scenario,ARRET_USB)
                        if(autorisation==1):
                            SERVOMOTEURS.activation_nourriture()
                            recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,pittag,autorisation,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
                
        if(scenario==9):
            while(ARRET_USB.stop_peripherique and WITTYPI.verification_horaire_systeme()):
                recompense=0
                SERVOMOTEURS.activation_porte()
                if(SERVOMOTEURS.verification_horaire_porte()):
                    LEDS.variation_pattern()
                    #if(True):
                    if(CAMERA.get_presence()==1):
                    #if(CAPTEUR_PIR.gestion_dectetion()==1 and CAMERA.get_presence()==1):
                    #if(BALANCE.get_weight()>1):
                        nbr_individu,heure_arrivee,ecart_visite=COMPTEUR.analyse_arrivee()
                        CAMERA.photo(str(nbr_individu))
                        CAMERA2.photo(str(nbr_individu))
                        #poids=BALANCE.get_weight()
                        SERVOMOTEURS.activation_nourriture()
                        recompense=BARRIERE_IR.recompense(ARRET_USB)
                        ENREGISTREMENT.set_ensemble_infos(jour,heure_arrivee,emplacement_of,nom_of,scenario,"Scénario sans Pittag",1,recompense,led1,led2,led3,led4,SERVOMOTEURS.get_etat_porte(),LEDS.get_pattern(),'Video_a_definir',ecart_visite)
    
    #Fin du while detection cle ou heure d'extinction de la mangeoire
    if(not(ARRET_USB.stop_peripherique)):
        print("Arrêt des modules, pour redémarrage")
        CAMERA.arret(1)
        CAMERA.free()
        CAMERA2.free()
        SERVOMOTEURS.arret_servo(1)
        SERVOMOTEURS.arret_servo(2)
        ARRET_USB.arret=1
        USB.arret=1
        GPIO.cleanup()
        print("Start again in 1 min") #20 secondes de temporisation plus le temps du lancement des périphériques
        time.sleep(20)
        run_again("python3 peripheriques.py")
        #subprocess.call('lxterminal -e python3 /home/pi/Mangeoire/peripheriques.py', shell=True)
    else:
        print("Arrêt des modules, pour traitement de l'IA")
        CAMERA.arret(1)
        CAMERA.free()
        CAMERA2.free()
        SERVOMOTEURS.arret_servo(1)
        SERVOMOTEURS.arret_servo(2)
        ARRET_USB.arret=1
        USB.arret=1
        GPIO.cleanup()
        ENREGISTREMENT.remove_infos_save()
        #traitement de l'IA
        subprocess.call(["bash","-c","source ~/.profile; "+'cd; cd Documents/tflite/; source bin/activate; python3 TFLite_detection_image.py --modeldir=models/model.tflite --labels=models/labelmap.txt --imagedir=/home/pi/Desktop/Images --keepDetections=True'])
        #transmission des informations par l'Xbee
           #TFLite_evaluation.py
           #TFLite_detection_image.py

    
    
def main(argv) :
    try:
        USB=Maintenance_USB()
        ARRET_USB=Redemarrage_post_maintenance(USB)
        traitement_scenario(ARRET_USB,USB) 
    except KeyboardInterrupt:
        print("Programme arrêté")
        #exit()
    return 0
if __name__ == "__main__":
    #main()
    sys.exit(main(sys.argv))
    