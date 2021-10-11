#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Config pour récupérer les informations du config.ini
import configparser
import datetime
import os
class Config :
    def __init__(self):
        self.config_ok=0
    
    def verification_dossier_images(self):
        if not os.path.isdir('/home/pi/Desktop/Images'):
            os.makedirs('/home/pi/Desktop/Images')
        
    
    def renvoie_config_general(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        scenario=cfg['scenario'].getint('num')
        nom=cfg['siteid'].get('nom')
        emplacement_of=cfg['siteid'].get('zone')
        probabilite_recompense=cfg['reward'].getint('probability')
        autorisation_recompense=cfg['reward'].getint('enable')
        sans_punition=cfg['punishment'].getint('without')
            
        return scenario, nom, emplacement_of, autorisation_recompense, probabilite_recompense,sans_punition
        
    def renvoie_config_servomoteurs(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        poucentage_open_position=cfg['door'].getint('open_position')
        poucentage_close_position=cfg['door'].getint('close_position') 
        pourcentage_ouverture_nourriture=cfg['food'].getint('pourcentage_ouverture_nourriture')
            
        return poucentage_open_position, poucentage_close_position, pourcentage_ouverture_nourriture

    def renvoie_config_horaire(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        heure_ouverture=cfg['time'].getint('wakeup_hour')
        min_ouverture=cfg['time'].getint('wakeup_minute')
        heure_fermeture=cfg['time'].getint('sleep_hour')
        min_fermeture=cfg['time'].getint('sleep_minute')
        porte_heure_ouverture=cfg['door'].getint('open_hour')
        porte_min_ouverture=cfg['door'].getint('open_minute')
        porte_heure_fermeture=cfg['door'].getint('close_hour')
        porte_min_fermeture=cfg['door'].getint('close_minute')
        delai_leds=cfg['attractiveleds'].getint('alt_delay')   
        on_hour=cfg['attractiveleds'].getint('on_hour')
        on_minute=cfg['attractiveleds'].getint('on_minute')
        off_hour=cfg['attractiveleds'].getint('off_hour')
        off_minute=cfg['attractiveleds'].getint('off_minute')
        delai_punition=cfg['punishment'].getint('delay')
        year=cfg['gendate'].getint('year')
        month=cfg['gendate'].getint('month')
        day=cfg['gendate'].getint('day')
        hour_transmission=cfg['communication'].getint('hour')
        min_transmission=cfg['communication'].getint('minute')
        horaire_transmission=datetime.timedelta(hours=hour_transmission, minutes=min_transmission)
        
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
            #AJOUTER HEURE DES LEDS DANS HORAIRES ALLUMAGE LEDS
        date_du_jour=datetime.date.today()
        date_debut_scenario= datetime.date(year, month, day)
        jour_ecoule=date_du_jour-date_debut_scenario
        jour_ecoule=jour_ecoule.days
        #print("Jour_ecoule",jour_ecoule.days)
        horaire_allumage=datetime.timedelta(hours=heure_ouverture, minutes=min_ouverture)
        horaire_extinction=datetime.timedelta(hours=heure_fermeture, minutes=min_fermeture)
        horaire_ouverture_porte=datetime.timedelta(hours=porte_heure_ouverture, minutes=porte_min_ouverture)
        horaire_fermeture_porte=datetime.timedelta(hours=porte_heure_fermeture, minutes=porte_min_fermeture)
        horaire_allumage_leds=datetime.timedelta(hours=on_hour, minutes=on_minute)
        horaire_extinction_leds=datetime.timedelta(hours=off_hour, minutes=off_minute)
        return horaire_allumage,horaire_extinction,horaire_ouverture_porte,horaire_fermeture_porte,horaire_allumage_leds,horaire_extinction_leds,delai_leds,delai_punition,jour_ecoule,horaire_transmission

    def renvoie_config_leds(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        pattern=cfg['attractiveleds'].getint('pattern')
        option_pattern=cfg['attractiveleds'].getint('option_pattern')
        random=cfg['attractiveleds'].getint('random')
        with_all=cfg['attractiveleds'].getint('with_all')
        one=cfg['attractiveleds'].getint('one')
        L_or_R=cfg['attractiveleds'].get('L_or_R')
        T_or_B=cfg['attractiveleds'].get('T_or_B')  
        c=cfg['attractiveleds'].getint('c')
        j=cfg['attractiveleds'].getint('j')
        phase=cfg['attractiveleds'].getint('phase')
            
        return pattern,option_pattern,L_or_R,T_or_B,one,random,with_all,c,j,phase

    def renvoie_couleurs_leds(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        ledr1=cfg['attractiveleds'].getint('red_1') 
        ledv1=cfg['attractiveleds'].getint('green_1')
        ledb1=cfg['attractiveleds'].getint('blue_1')
        ledr2=cfg['attractiveleds'].getint('red_2') 
        ledv2=cfg['attractiveleds'].getint('green_2')
        ledb2=cfg['attractiveleds'].getint('blue_2')
        ledr3=cfg['attractiveleds'].getint('red_3') 
        ledv3=cfg['attractiveleds'].getint('green_3')
        ledb3=cfg['attractiveleds'].getint('blue_3')
        ledr4=cfg['attractiveleds'].getint('red_4') 
        ledv4=cfg['attractiveleds'].getint('green_4')
        ledb4=cfg['attractiveleds'].getint('blue_4')
        ledrall=cfg['attractiveleds'].getint('red_all') 
        ledvall=cfg['attractiveleds'].getint('green_all')
        ledball=cfg['attractiveleds'].getint('blue_all')
        
        return ledr1,ledv1,ledb1,ledr2,ledv2,ledb2,ledr3,ledv3,ledb3,ledr4,ledv4,ledb4,ledrall,ledvall,ledball
        
    def renvoie_config_pittags(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        rfid_actif=cfg['listepittag'].getint('rfid_actif')
        facteur_division=cfg['listepittag'].getint('facteur_division')
        portion_de_debut=cfg['listepittag'].getint('portion_de_debut')
        phase_rfid=cfg['listepittag'].getint('phase')
        heure_duree_portion=cfg['listepittag'].getint('heure_duree_portion')
        min_duree_portion=cfg['listepittag'].getint('min_duree_portion')
        seconds_duree_portion=cfg['listepittag'].getint('seconds_duree_portion')
        duree_par_portion=datetime.timedelta(hours=heure_duree_portion, minutes=min_duree_portion,seconds=seconds_duree_portion)
            
        return facteur_division, portion_de_debut, phase_rfid, duree_par_portion
    
    def modifier_config_scenario_5(self):
        cfg = configparser.ConfigParser()
        cfg.read('/home/pi/Desktop/config/CONFIG.INI')
        date_du_jour=datetime.date.today()
        phase=cfg['attractiveleds'].getint('phase')
        year=cfg['gendate'].getint('year')
        month=cfg['gendate'].getint('month')
        day=cfg['gendate'].getint('day')
        date_debut_scenario= datetime.date(year, month, day)
        jour_ecoule=date_du_jour-date_debut_scenario
        c=cfg['attractiveleds'].getint('c')
        j=cfg['attractiveleds'].getint('j')
        facteur_division=cfg['listepittag'].getint('facteur_division')
        portion_de_debut=cfg['listepittag'].getint('portion_de_debut')
        date_du_jour=datetime.date.today()
        date_debut_scenario= datetime.date(year, month, day)
        jour_ecoule=date_du_jour-date_debut_scenario
        #print("jour_ecoule",jour_ecoule)
        if(jour_ecoule.days==j):
            cfg.set('attractiveleds','j','1')
            if(c==0):
                cfg.set('attractiveleds','c','1')
            else:
                cfg.set('attractiveleds','c','0')

            if(phase==1):
                if(portion_de_debut<facteur_division):
                    portion_de_debut=portion_de_debut+1
                    cfg.set('listepittag','portion_de_debut',str(portion_de_debut))
                else:
                    portion_de_debut=1
                    cfg.set('listepittag','portion_de_debut',str(portion_de_debut))
            if(phase==3):#jour_ecoule%2==0 rajouter la condition plus la variable jour_ecoule
                if(jour_ecoule.days%2==0):
                    if(portion_de_debut<facteur_division):
                        portion_de_debut=portion_de_debut+1
                        cfg.set('listepittag','portion_de_debut',str(portion_de_debut))
                    else:
                        portion_de_debut=1
                        cfg.set('listepittag','portion_de_debut',str(portion_de_debut))
                        
        else:
            j=j+1
            cfg.set('attractiveleds','j',str(j))
        
        with open ('/home/pi/Desktop/config/CONFIG.INI','w') as configfile:
            cfg.write(configfile)
            
            
"""    
def main() :
    scenario, nom, emplacement_of, autorisation_recompense, probabilite_recompense=renvoie_config_general()
    horaire_allumage,horaire_extinction,horaire_ouverture_porte,horaire_fermeture_porte,horaire_allumage_leds,horaire_extinction_leds,delai_leds,delai_punition=renvoie_config_horaire()
    pattern,option_pattern,ledr1,ledv1,ledb1,ledr2,ledv2,ledb2,ledr3,ledv3,ledb3,ledr4,ledv4,ledb4,ledrall,ledvall,ledball,L_or_R,T_or_B,one=renvoie_config_leds()
    facteur_division, portion_de_debut=renvoie_config_pittags()
    
if __name__ == "__main__":
    main()
"""
