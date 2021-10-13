# Création de la classe Leds
import RPi.GPIO as GPIO
import time
import datetime
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

led1r=GPIO.PWM(16,50)
led1g=GPIO.PWM(20,50)
led1b=GPIO.PWM(21,50)
led1r.start(0)
led1g.start(0)
led1b.start(0)
led1r.ChangeDutyCycle(100)
led1g.ChangeDutyCycle(0)
led1b.ChangeDutyCycle(0)

time.sleep(6)
led1r.stop(0)
led1g.stop(0)
led1b.stop(0)

GPIO.cleanup()
