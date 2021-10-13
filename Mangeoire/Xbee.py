#!/usr/bin/env python3

# Copyright (C) 2021  Malik Irain
# This file is part of econect-i8-utils.
#
# econect-i8-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# econect-i8-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with econect-i8-utils.  If not, see <http://www.gnu.org/licenses/>.


from sys import argv, exit
from time import sleep
import datetime
#from typing import Final

#from config import EXAMPLES_DIR, EXAMPLES_FILES, LOG_DIR
#from econect.formats import NeoCayenneLPP
from econect.protocol.I8TL import DataSender

class Xbee:
    def __init__(self):
        self.devfile : str = "/dev/ttyUSB0"
        self.bauds   : int = 230400
        self.log_dir : str = "/home/pi/Desktop/econect-xbee/src/log"
        self.horaire_extinction=datetime.timedelta(hours=0, minutes=0)
    def envoie_fichier(self):
        if len(argv) > 1:
            self.devfile = argv[1]
        if len(argv) > 2:
            file_to_send = argv[2]
        ds : DataSender = DataSender(path=self.devfile, speed=self.bauds, del_dir=True, self_stop=True, qos_info=True, log_dir=self.log_dir, response_timeout=1, retries=3)
        heures_actuelles=datetime.datetime.now().hour
        minutes_actuelles=datetime.datetime.now().minute
        horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
        i : int = 0
        cinq_minutes=datetime.timedelta(hours=0, minutes=5)
        while horaire_actuelle<self.horaire_extinction+cinq_minutes:
            heures_actuelles=datetime.datetime.now().hour
            minutes_actuelles=datetime.datetime.now().minute
            horaire_actuelle=datetime.timedelta(hours=heures_actuelles, minutes=minutes_actuelles)
            ds.notify_file_to_send('/home/pi/Desktop/sauvegardes.csv')
            i = (i+1)%len('/home/pi/Desktop/sauvegardes.csv')
            sleep(10)