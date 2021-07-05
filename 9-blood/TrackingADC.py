import RPi.GPIO as GPIO
import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comparator = 4 
troykaVoltage = 17

bits = len(dac)
levels = 2 ** bits
dV = 3.3 / levels

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds + dac, GPIO.OUT)
GPIO.setup(troykaVoltage, GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)

def num2pins(pins, value):
    GPIO.output(pins, [int(i) for i in bin(value)[2:].zfill(bits)])

def adc2():

    timeout = 0.001
    value = 128
    delta = 128

    for i in range(8):
        num2pins(dac, value)
        time.sleep(timeout)

        direction = -1 if (GPIO.input(comparator) == 0) else 1
        
        num = delta * direction / 2
        
        # print(value, num, delta, direction)
        
        value = int(value + num)
        delta = delta / 2

    # print(value)
    return value


def trackingADC():
    
    U = adc2() + 1

    if GPIO.input(comparator) == 0:
        while GPIO.input(comparator) == 0:
            U -= 1
            break

    if  GPIO.input(comparator) == 1:
        while GPIO.input(comparator) == 1:
            U -= 1
            break
    return U 

try:
    while True:
        print(trackingADC())
        
finally:
    GPIO.cleanup()