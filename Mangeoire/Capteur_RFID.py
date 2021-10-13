# coding: utf-8
# Création de la classe Capteur_RFID
import RPi.GPIO as GPIO
import time
import datetime
import csv
from math import ceil
from rfid import RFID
#from pirc522 import RFID

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Capteur_RFID :
    def __init__(self):
        self.rc522 = RFID()
        self.uid=[]
        self.facteur_division=0
        self.portion_de_debut=0
        self.temps_portion_ecoule=datetime.timedelta(hours=0, minutes=0, seconds=0)
        self.horaire_init=datetime.timedelta(hours=datetime.datetime.now().hour, minutes=datetime.datetime.now().minute, seconds=datetime.datetime.now().second)
        self.reussite_lecture=False
        self.arret=False
        self.jour_ecoule=0
        self.phase=0
        self.nom_OF=''
        self.numero_rfid=[]
        self.nombre_venu=[]
        self.rfid_actif=0
       
    def lecture_badge(self,ARRET_USB):
        timer=0
        val_lue=0
        self.reussite_lecture=False
        while timer<50 and val_lue==0 and ARRET_USB.stop_peripherique :
            timer=timer+1
            #self.rc522.wait_for_tag() #On attend qu'une puce RFID passe à portée pendant timer
            (error, tag_type) = self.rc522.request() #Quand une puce a été lue, on récupère ses infos
            if not error : #Si on a pas d'erreur
                (error, uid) = self.rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
                if not error : #Si on a réussi à nettoyer
                    self.uid=uid
                    val_lue=1
                    print("Vous avez passé le badge avec l'id : {}".format(uid)) #On affiche l'identifiant unique du badge RFID
                    self.reussite_lecture=True
                    #return True
                    time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-s
        if(ARRET_USB.stop_peripherique==False):
            self.arret=True
                    
        #return False
        
    def verif_bdd_oiseau(self):
        f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID 
        fichierCSV= csv.reader(f)
        elem=[0,0,0,0,0]
        pittag=0
        sortie=False
        for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
            #print("Voici la taille d'une ligne",len(ligne))
            if(len(ligne)==12):
                elem[0]=int(ligne[0])
                elem[1]=int(ligne[1])
                elem[2]=int(ligne[2])
                elem[3]=int(ligne[3])
                elem[4]=int(ligne[4])
                if(elem==self.uid):#Verifie l'uid du badge lu avec la ligne de la base de donnée
                    pittag=str(elem)
                    sortie=True#self.autorisation_oiseau=True
                    valr=int(ligne[5])
                    valg=int(ligne[6])
                    valb=int(ligne[7])
                    L_or_R=ligne[8]
                    T_or_B=ligne[9]
                    One=int(ligne[10])
                    Nom_OF_Oiseau=ligne[11]
                elem=[0,0,0,0,0]
            elif(sortie==False):
                valr=0
                valg=0
                valb=0
                L_or_R='L'
                T_or_B='T'
                One=0
                Nom_OF_Oiseau="Undefined"
        reussite_verif=sortie
        if(self.reussite_lecture==True and reussite_verif==True):
            autorisation=1
        elif(self.reussite_lecture==False ):
            autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
            pittag="XXXXXXXX"
        elif(reussite_verif==False):
            autorisation=0
            pittag="????????"
        
            
        return autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau#Faire dans l'objet périphérique un condition tq si et seulement si sortie est True on active l'autorisation de manger
    
    
    def variation_temporelle(self):
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        secondes_actuelles=datetime.datetime.now().second
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles, seconds=secondes_actuelles) 
        #Verifier l'heure et le temps passée 
        if(horaire_actuelle>self.horaire_init+self.temps_portion_ecoule):
            self.portion_de_debut=self.portion_de_debut+1 #incrementation de la portion de la partie de la liste d'oiseaux autorisées
            self.horaire_init=horaire_actuelle
            if(self.portion_de_debut>self.facteur_division):
                self.portion_de_debut=1
        
    
    def cas_scenario_4(self): #de cb diviser la liste d'oiseau att inf au nbre de ligne, à quel partie on veut commencer, et le temps avant incrémentation de la portion
        f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID
        text=f.readlines()
        fichierCSV= csv.reader(f)
        elem=[0,0,0,0,0]
        autorisation=0
        sortie=False
        NumberOfLine = len(text)
        intervalsup=int(ceil(NumberOfLine/self.facteur_division))*self.portion_de_debut
        intervalinf=int(ceil(NumberOfLine/self.facteur_division))*(self.portion_de_debut-1)
        file=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv')
        fichierCSV= csv.reader(file)
        nbligne=0
        for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
            nbligne=nbligne+1
            elem[0]=int(ligne[0])
            elem[1]=int(ligne[1])
            elem[2]=int(ligne[2])
            elem[3]=int(ligne[3])
            elem[4]=int(ligne[4])
            if(elem==self.uid):
                if(nbligne >= intervalinf and nbligne <= intervalsup):
                    autorisation=1
                    sortie=True
                pittag=elem
            elem=[0,0,0,0,0]
        reussite_verif=sortie
        if(self.reussite_lecture==True and reussite_verif==True):
            autorisation=1
        elif(self.reussite_lecture==False ):
            autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
            pittag="XXXXXXXX"
        elif(reussite_verif==False):
            autorisation=0
            pittag="????????"
        return autorisation,pittag
  
    def cas_scenario_5(self): #de cb diviser la liste d'oiseau att inf au nbre de ligne, à quel partie on veut commencer, et le temps avant incrémentation de la portion
        #Temps de portion ecoule
        if(self.phase==1 or self.phase==3):
            f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID
            text=f.readlines()
            fichierCSV= csv.reader(f)
            elem=[0,0,0,0,0]
            autorisation=0
            sortie=False
            NumberOfLine = len(text)
            intervalsup=int(ceil(NumberOfLine/self.facteur_division))*self.portion_de_debut
            intervalinf=int(ceil(NumberOfLine/self.facteur_division))*(self.portion_de_debut-1)
            file=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv')
            fichierCSV= csv.reader(file)
            nbligne=0
            for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
                nbligne=nbligne+1
                elem[0]=int(ligne[0])
                elem[1]=int(ligne[1])
                elem[2]=int(ligne[2])
                elem[3]=int(ligne[3])
                elem[4]=int(ligne[4])
                if(elem==self.uid):
                    if(nbligne >= intervalinf and nbligne <= intervalsup):
                        autorisation=1
                        sortie=True
                    pittag=elem
                elem=[0,0,0,0,0]
            reussite_verif=sortie
            if(self.reussite_lecture==True and reussite_verif==True):
                autorisation=1
            elif(self.reussite_lecture==False ):
                autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
                pittag="XXXXXXXX"
            elif(reussite_verif==False):
                autorisation=0
                pittag="????????"
            return autorisation,pittag            
        if(self.phase==2):
            heures_actuelles=datetime.datetime.now().hour
            minutes_actuelles=datetime.datetime.now().minute
            seconds_actuelles=datetime.datetime.now().second
            horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles, seconds=seconds_actuelles)
            #Verifier l'heure et le temps passée 
            if(horaire_actuelle>self.horaire_init+self.temps_portion_ecoule):
                self.portion_de_debut=self.portion_de_debut+1 #incrementation de la portion de la partie de la liste d'oiseaux autorisées
                #self.horaire_init=horaire_actuelle
                if(self.portion_de_debut>self.facteur_division):
                    self.portion_de_debut=1
            f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID
            text=f.readlines()
            fichierCSV= csv.reader(f)
            elem=[0,0,0,0,0]
            autorisation=0
            sortie=False
            NumberOfLine = len(text)
            intervalsup=int(ceil(NumberOfLine/self.facteur_division))*self.portion_de_debut
            intervalinf=int(ceil(NumberOfLine/self.facteur_division))*(self.portion_de_debut-1)
            file=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv')
            fichierCSV= csv.reader(file)
            nbligne=0
            for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
                nbligne=nbligne+1
                elem[0]=int(ligne[0])
                elem[1]=int(ligne[1])
                elem[2]=int(ligne[2])
                elem[3]=int(ligne[3])
                elem[4]=int(ligne[4])
                if(elem==self.uid):
                    if(nbligne >= intervalinf and nbligne <= intervalsup):
                        autorisation=1
                        sortie=True
                    pittag=elem
                elem=[0,0,0,0,0]
            reussite_verif=sortie
            if(self.reussite_lecture==True and reussite_verif==True):
                autorisation=1
            elif(self.reussite_lecture==False ):
                autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
                pittag="XXXXXXXX"
            elif(reussite_verif==False):
                autorisation=0
                pittag="????????"
            return autorisation,pittag    
      
    def cas_scenario_6(self):
        if(self.phase==1):#changer phase type
            f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID
            fichierCSV= csv.reader(f)
            elem=[0,0,0,0,0]
            pittag=0
            acces_possible=0
            for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
                #print("Voici la taille d'une ligne",len(ligne))
                if(len(ligne)==12):
                    elem[0]=int(ligne[0])
                    elem[1]=int(ligne[1])
                    elem[2]=int(ligne[2])
                    elem[3]=int(ligne[3])
                    elem[4]=int(ligne[4])
                    Nom_OF_Oiseau=ligne[11]
                    #print("elem",elem,"self.iud",self.uid)
                    if(elem==self.uid):#Verifie l'uid du badge lu avec la ligne de la base de donnée
                        pittag=elem
                        acces_possible=1
                    elem=[0,0,0,0,0]
            print("Nom_OF",self.nom_OF)
            print("Nom_OF_Oiseau",Nom_OF_Oiseau)
            print("Condition result",self.nom_OF==Nom_OF_Oiseau and acces_possible==1)
            if(self.nom_OF==Nom_OF_Oiseau and acces_possible==1):
                reussite_verif=True
            else:
                reussite_verif=False
            if(self.reussite_lecture==True and reussite_verif==True):
                autorisation=1
            if(self.reussite_lecture==False ):
                autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
                pittag="XXXXXXXX"
            if(self.reussite_lecture==True and reussite_verif==False):
                autorisation=0
                pittag="????????"
            return autorisation,pittag 
        
        if(self.phase==2):
            f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID 
            fichierCSV= csv.reader(f)
            elem=[0,0,0,0,0]
            pittag=0
            case=0
            sortie=False
            for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
                #print("Voici la taille d'une ligne",len(ligne))
                if(len(ligne)==12):
                    elem[0]=int(ligne[0])
                    elem[1]=int(ligne[1])
                    elem[2]=int(ligne[2])
                    elem[3]=int(ligne[3])
                    elem[4]=int(ligne[4])
                    Nom_OF_Oiseau=ligne[11]
                    if(elem==self.uid):#Verifie l'uid du badge lu avec la ligne de la base de donnée
                        pittag=elem
                        for i in self.numero_rfid: #parcours toutes les cases du tableau du numero de rfid
                            if(i==elem): #si celui-ci vaut le numéro rfid lu
                                if(self.nombre_venu[case]==0):
                                    self.nombre_venu[case]=1
                                    acces_possible=1
                                else:
                                    acces_possible=0
                            case=case+1   
                    elem=[0,0,0,0,0]
            if(acces_possible==1):
                reussite_verif=True
            else:
                reussite_verif=False
            if(self.reussite_lecture==True and reussite_verif==True):
                autorisation=1
            if(self.reussite_lecture==False ):
                autorisation=1 #On l'autorise car c'est la lecture de la carte qui n'a pas fonctionné mais on ne saura pas qui c'est ou si il avait un pittag
                pittag="XXXXXXXX"
            if(self.reussite_lecture==True and reussite_verif==False):
                autorisation=0
                pittag="????????"
            print("autorisation",autorisation,"pittag",pittag)
            return autorisation,pittag 
            

    def pittags_gestionnaire(self,scenario,ARRET_USB):
        if(self.rfid_actif==1):
            self.lecture_badge(ARRET_USB) #Récupère la réussite de la lecture du badge
            if(self.arret):
                if(scenario!=4 and scenario!=5 and scenario!=6 and scenario>1):
                    autorisation=0
                    pittag="????????"
                    valr=""
                    valg=""
                    valb=""
                    L_or_R=""
                    T_or_B=""
                    One=""
                    Nom_OF_Oiseau=""
                    return autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau
                else:
                    autorisation=0
                    pittag="????????"
                    return autorisation,pittag
            else:
                if(scenario!=4 and scenario!=5 and scenario!=6 and scenario>1):
                    autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau=self.verif_bdd_oiseau() #Récupère la réussite de la correspondance avec un oiseau
                    return autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau
                if(scenario==4):
                    autorisation,pittag=self.cas_scenario_4()
                    return autorisation,pittag
                if(scenario==5):
                    autorisation,pittag=self.cas_scenario_5()
                    return autorisation,pittag
                if(scenario==6):
                    print("self.phase",self.phase)
                    autorisation,pittag=self.cas_scenario_6()
                    return autorisation,pittag
        else:
            if(scenario!=4 and scenario!=5 and scenario!=6 and scenario>1):
                valr=""
                valg=""
                valb=""
                L_or_R=""
                T_or_B=""
                One=""
                Nom_OF_Oiseau=""
                autorisation=1
                pittag="????????"
                return autorisation,pittag,valr,valg,valb,L_or_R,T_or_B,One,Nom_OF_Oiseau
            else:
                autorisation=1
                pittag="????????"
                return autorisation,pittag
            
    def set_phase(self,x):
        self.phase=x
    def get_phase(self):
        return self.phase
    def set_jour_ecoule(self,x):
        self.jour_ecoule=x
    def get_jour_ecoule(self):
        return self.jour_ecoule   
    def set_nom_OF(self,x):
        self.nom_OF=x
    def get_nom_OF(self):
        return self.nom_OF
    def set_facteur_division(self,x):
        self.facteur_division=x
    def get_facteur_division(self):
        return self.facteur_division
    def set_portion_de_debut(self,x):
        self.portion_de_debut=x
    def get_portion_de_debut(self):
        return self.portion_de_debut
    def set_temps_portion_ecoule(self,x):
        self.temps_portion_ecoule=x
    def get_temps_portion_ecoule(self):
        return self.temps_portion_ecoule
    def set_pittag_choices(self,facteur_division, portion_de_debut,duree_par_portion,rfid_actif):
        self.facteur_division=facteur_division
        self.portion_de_debut=portion_de_debut
        self.rfid_actif=rfid_actif
        self.temps_portion_ecoule=duree_par_portion
        
    def init_scenario_6(self):
        f=open('/home/pi/Desktop/bdd_rfid_oiseaux.csv') #Ouvre le fichier csv la base de donnée des RFID 
        fichierCSV= csv.reader(f)
        elem=[0,0,0,0,0]

        for ligne in fichierCSV:# Lis ligne par ligne le fichier csv
            #print("Voici la taille d'une ligne",len(ligne))
            if(len(ligne)==12):
                elem[0]=int(ligne[0])
                elem[1]=int(ligne[1])
                elem[2]=int(ligne[2])
                elem[3]=int(ligne[3])
                elem[4]=int(ligne[4])
                self.numero_rfid.extend([elem])
                self.nombre_venu.extend([0])
                elem=[0,0,0,0,0]

    def set_horaire_init(self,x):
        self.horaire_init=x
        
    def get_horaire_init(self,x):
        return self.horaire_init
    

        
        
        
