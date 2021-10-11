#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time


#Set function to calculate percent from angle
def percent_to_angle (pourcentage) :
    if (pourcentage < 0 or pourcentage > 100 ):
        raise Exception("Le pourcentage n'est pas dans l'intervalle [0;100]")
    
    value=1.1 +(11.7-1.1)*pourcentage/100.0

    return value


GPIO.setmode(GPIO.BCM) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings

#Use pin 12 for PWM signal
pwm_gpio = 18
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

#Init at 0°
pwm.start(percent_to_angle(0))
time.sleep(1)

#Go at 90°
pwm.ChangeDutyCycle(percent_to_angle(50))
time.sleep(1)

#Finish at 180°
pwm.ChangeDutyCycle(percent_to_angle(100))
time.sleep(1)

#Close GPIO & cleanup
pwm.stop()
GPIO.cleanup()