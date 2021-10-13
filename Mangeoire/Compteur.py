#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Compteur
import datetime

class Compteur :
    def __init__(self):
        self.ecart_visite="Pas encore d'écart"
        self.date_time=datetime.datetime.now()
        self.heure_dernier_oiseau=datetime.datetime.now()
        self.nbr_individu=0
        self.heur_arrivee=0
    
    def comptage_individu_passes(self):
        self.nbr_individu=self.nbr_individu+1
        self.date_time=datetime.datetime.now()
        self.heure_arrivee=self.date_time.strftime("%H_%M_%S")
        return self.nbr_individu,self.heure_arrivee
    
    def determination_ecart_de_passage(self):
        if(self.nbr_individu>1):
            self.ecart_visite=self.date_time-self.heure_dernier_oiseau
            self.heure_dernier_oiseau=self.date_time
        else:
            self.heure_dernier_oiseau=self.date_time
        return self.ecart_visite
    def analyse_arrivee(self):
        nbr_individu, heure_arrivee=self.comptage_individu_passes()
        ecart_visite=self.determination_ecart_de_passage()
        return nbr_individu,heure_arrivee, ecart_visite