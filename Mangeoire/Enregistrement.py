#! /usr/bin/env python3
# coding: utf-8
# Création de la classe Enregistrement
import csv
import os

class Enregistrement:
    def __init__(self):
        self.ligne_en_cours=0
    def set_ensemble_infos(self,inf1,inf2,inf3,inf4,inf5,inf6,inf7,inf8,inf9,inf10,inf11,inf12,inf13,inf14,inf15,inf16):
        if not os.path.isdir('/home/pi/Desktop/sauvegardes.csv'):
            os.makedirs('/home/pi/Desktop/sauvegardes.csv')
        with open('/home/pi/Desktop/sauvegardes.csv','a',encoding='UTF8') as f:
            fieldnames=['Jour','Heure','Emplacement_OF','Nom_OF','ID_Scenario','PIT_Tag','Autorisation_passage','Prise_de_récompense','Valeur_RGB_LED1','Valeur_RGB_LED2','Valeur_RGB_LED3','Valeur_RGB_LED4','Etat_courant_porte','Pattern_LED','Video','Ecart_temps_individu']
            writer=csv.DictWriter(f,fieldnames=fieldnames)
            writer.writerow({'Jour':str(inf1),'Heure':str(inf2),'Emplacement_OF':str(inf3),'Nom_OF':str(inf4),'ID_Scenario':str(inf5),'PIT_Tag':str(inf6),'Autorisation_passage':str(inf7),'Prise de récompense':str(inf8),'Valeur_RGB_LED1':str(inf9),'Valeur_RGB_LED2':str(inf10),'Valeur_RGB_LED3':str(inf11),'Valeur_RGB_LED4':str(inf12),'Etat_courant_porte':str(inf13),'Pattern_LED':str(inf14),'Video':inf15,'Ecart_temps_individu':str(inf16)})
            f.close()
    def remove_infos_save(self):
        with open('/home/pi/Desktop/sauvegardes.csv',"r+") as file:
            file.truncate(4)
            file.close()
            
    def fusion_des_csv(self):
        with open('/home/pi/Documents/tflite/CSV_analyse_IA.csv','r') as file:
            f=csv.reader(file)
            data=[]
            for row in f:
                data.append(row)
            header=data[0]
            rows=data[1:]
            rows.sort(reverse=False)

        with open('/home/pi/Desktop/sauvegardes.csv','a',newline='') as file_out:
            f=csv.writer(file_out)
            f.writerow(header)
            f.writerows(rows)

        if os.path.exists('/home/pi/Documents/tflite/CSV_analyse_IA.csv'):
            os.remove('/home/pi/Documents/tflite/CSV_analyse_IA.csv')
