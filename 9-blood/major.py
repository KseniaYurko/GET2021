import RPi.GPIO as GPIO
import time
import numpy as np
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

try:
  
    measure = []
    value = 0

    barr = int(input('Barr: '))
    
    start = time.time()

    GPIO.output(troykaVoltage, 1)

    while time.time() - start <= 10:
        value = adc2()
        measure.append(value)

    #print (len(measure))
    mean = sum(measure)/len(measure)

    np.savetxt('5-adc-measure/calibration_{}.txt'.format(mean),measure, fmt='%d')
    with open('adc{}'.format(barr), 'w') as adcX:
        adcX.write(str(mean))
    with open('barr{}'.format(barr), 'w') as barrX:
        barrX.write(str(barr))
    print('Done! Files already saved!')

finally:
    GPIO.cleanup()
    print('GPIO cleanup completed.')