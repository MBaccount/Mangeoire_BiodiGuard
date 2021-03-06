#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFFFFF, 0x9400D3]
pins = {'pin_R':23, 'pin_G':7, 'pin_B':25}  # pins is a dict

GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   # For example : col = 0x112233
        R_val = (col & 0x110000) >> 16
        G_val = (col & 0x001100) >> 8
        B_val = (col & 0x000011) >> 0

        R_val = map(R_val, 100, 255, 0, 0)
        G_val = map(G_val, 100, 255, 0, 0)
        B_val = map(B_val, 100, 255, 0, 0)

        p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
        p_G.ChangeDutyCycle(100-G_val)
        p_B.ChangeDutyCycle(100-B_val)

try:
        while True:
                for col in colors:
                        setColor(col)
                        time.sleep(1.0)
except KeyboardInterrupt:
        p_R.stop()
        p_G.stop()
        p_B.stop()
        for i in pins:
                GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
        GPIO.cleanup()