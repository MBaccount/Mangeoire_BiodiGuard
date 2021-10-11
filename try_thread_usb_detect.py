from threading import Thread
import os
import os.path
import re
import subprocess
import sys
import glob
import shutil
from time import sleep  
class Maintenance_USB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.copie=0 
        self.utile_seulement=[] 
        self.init=[]
        self.arret=0
        self.cle_usb_presente=0
        self.start()
    
    def arret(self,x):
        self.arret=x
        
    def run(self):
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i.decode())   
                #print(info)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '%s%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    self.init.append(dinfo['device'])
        while self.arret==0:
            device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
            df = subprocess.check_output("lsusb")
            
            for i in df.split(b'\n'):
                if i:
                    info = device_re.match(i.decode())   
                    #print(info)
                    if info:
                        dinfo = info.groupdict()
                        dinfo['device'] = '%s%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                        self.utile_seulement.append(dinfo['device'])
            #print("Valeur de copie",self.copie)
                        #"""
            if(self.init!=self.utile_seulement and self.copie==0):
                sleep(8)
                if glob.glob("/media/pi/*") is not None:
                    var=glob.glob("/media/pi/*")
                    #print("var",var)
                    if(var!=[]):
                        nom_de_la_cle=var[0].replace("/media/pi/",'')
                        print("nom_de_la_cle",nom_de_la_cle)
                    else:
                        nom_de_la_cle='null'
                    src = '/media/pi/'+nom_de_la_cle+'/CONFIG.INI'
                    dst = '/home/pi/Desktop/config'+'/CONFIG.INI'
                    if(os.path.isfile(src)):
                        shutil.copyfile(src, dst)
                        print("Retirez le dispositif de stockage")
                        self.copie=1
                    else:
                        print("Le fichier CONFIG.INI n'est pas sur le dispositif de stockage")
                    self.cle_usb_presente=1
                    #print("Valeur de copie",self.copie)
             
            elif(self.init==self.utile_seulement and self.copie==1):
                self.cle_usb_presente=0
                self.copie=0
                break
            self.utile_seulement=[]
            #"""

class Redemarrage_post_maintenance(Thread):
    def __init__(self,Maintenance_USB):
        Thread.__init__(self)
        self.daemon = True
        self.arret=0
        self.Maintenance_USB=Maintenance_USB
        self.stop_peripherique=True
        self.autorisation_redemarrage=0
        self.start()
        
    def arret(self,x):
        self.arret=x
        
    def run(self):
        while self.arret==0:
            if self.Maintenance_USB.copie==1:
                self.stop_peripherique=False
                """
            if self.Maintenance_USB.copie==0:
                self.stop_peripherique=True
                """
                
            """
            print("Auto start du systeme")
            subprocess.call('lxterminal -e python3 /home/pi/Mangeoire/peripheriques.py', shell=True)
            """
            
