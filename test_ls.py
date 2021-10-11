import os
import subprocess
import glob
import shutil

var=glob.glob("/media/pi/*")
nom_de_la_cle=var[0].replace("/media/pi/",'')
src = '/media/pi/'+nom_de_la_cle+'/CONFIG.INI'
dst = '/home/pi/Desktop/config'+'/CONFIG.INI'
if(os.path.isfile(src)):
    shutil.copyfile(src, dst)
    print("Le fichier a bien été copié")
else:
    print("Le fichier CONFIG.INI n'est pas présent sur la clé ou ne possède pas ce nom ")