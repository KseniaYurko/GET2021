# Import modules (prepare script)

import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

# Create variables that will not change in our script ("constants")

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comparator = 4 
troykaVoltage = 17

bits = len(dac)
levels = 2 ** bits
dV = 3.3 / levels

# Setup GPIO for this run of the script

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds + dac, GPIO.OUT)
GPIO.setup(troykaVoltage, GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)


# Define functions for this run of the script

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
        value = int(value + num)
        delta = delta / 2

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

# "Try block" with all your "application" or "user" logic

try:
    # 1. Create variables

    measure = []
    timeline = []
    value = 0

    # 2. Fix start time
    
    start = time.time()

    # 3. Charge capacitor
    
    GPIO.output(troykaVoltage, 1)
    
    while time.time() - start <= 20:
        value = adc2()
        measure.append(value)
        timeline.append(round(time.time()-start, 2))

    # 4. Open calibration files and transition to bars

    with open('adc160', 'r') as adc1:
        a1 = float(adc1.read())
    with open('barr160', 'r') as barr1:
        b1 = float(barr1.read())
    with open('adc40', 'r') as adc2:
        a2 = float(adc2.read())
    with open('barr40', 'r') as barr2:
        b2 = float(barr2.read())
 
    k = (a1-a2)/(b1-b2)
    measure = [i*k for i in measure]

    # 5. Fix finish time and print time values

    finish = time.time()

    totalTime = finish - start
    measurePeriod = totalTime / len(measure)
    samplingFrequency = int(1 / measurePeriod)

    print("Total measure time: {:.2f} s, measure period: {:.3f} ms, sampling frequency: {:d} Hz".format(totalTime, measurePeriod, samplingFrequency))
    print("Voltage step: {:.3f} V".format(dV))

    # 6. Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set(title = 'График давления',
            xlabel = 'Время, с',
            ylabel = 'Давление, мм.рт.ст.')

    ax.grid(which='major',
            color = 'k')
            
    ax.grid(which='minor',
            color = 'gray',
            linestyle = ':')

    ax.plot(timeline, measure)
    
    plt.show()

    fig.savefig('/home/pi/Repositories/get/9-blood/Data/Plot')
    np.savetxt('/home/pi/Repositories/get/9-blood/Data/DATA.txt', measure, fmt='%d')
    np.savetxt('/home/pi/Repositories/get/9-blood/Data/TIME.txt', timeline, fmt='%1.2f')
    print('Done! Files already saved!')

# "Finally block" with functions that must be execute after script any way

finally:
    GPIO.cleanup()
    print('GPIO cleanup completed.')