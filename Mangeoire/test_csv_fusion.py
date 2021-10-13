#! /usr/bin/env python3
# coding: utf-8
# Création de la classe test
import csv
import sys
import os

with open('/home/pi/Documents/tflite/analyse_IA.csv','r') as file:
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

if os.path.exists('/home/pi/Documents/tflite/analyse_IA.csv'):
    os.remove('/home/pi/Documents/tflite/analyse_IA.csv')