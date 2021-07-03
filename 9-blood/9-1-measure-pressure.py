# Script starts to run right here!
# Yes, script is already running!

################################################################################
# Import modules (prepare script)
################################################################################

import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt


################################################################################
# Create variables that will not change in our script ("constants") 
################################################################################

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comparator = 4 
troykaVoltage = 17

bits = len(dac)
levels = 2 ** bits
dV = 3.3 / levels


################################################################################
# Setup GPIO for this run of the script
################################################################################

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds + dac, GPIO.OUT)
GPIO.setup(troykaVoltage, GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)


################################################################################
# Define functions for this run of the script
################################################################################

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

def adc():

    timeout = 0.0001
    value = 0
    direction = 1

    for i in range(8):
        delta = 2 ** (8 - i - 1)
        value += delta * direction

        num2pins(dac, value)
        time.sleep(timeout)

        direction = -1 if (GPIO.input(comparator) == 0) else 1

    value += 1 if direction > 0 else 0

    return value


# Main logic of the script starts only here!

################################################################################
# "Try block" with all your "application" or "user" logic
################################################################################

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
        # num2pins(leds, value)
        measure.append(value)
        timeline.append(round(time.time()-start, 2))

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
 
    # 4. Discharge capacitor

    # GPIO.output(troykaVoltage, 0)

    # while value > 1:
    # value = adc()
    # num2pins(leds, value)
    # measure.append(value)

    # 5. Fix finish time and print time values

    finish = time.time()

    totalTime = finish - start
    measurePeriod = totalTime / len(measure)
    samplingFrequency = int(1 / measurePeriod)

    print("Total measure time: {:.2f} s, measure period: {:.3f} ms, sampling frequency: {:d} Hz".format(totalTime, measurePeriod, samplingFrequency))
    print("Voltage step: {:.3f} V".format(dV))

    # 6. Plot results


    plt.plot(timeline, measure)
    plt.title('График давления')
    plt.xlabel('Время, с')
    plt.ylabel('Давление, Барр')
    plt.show()
    time.sleep(10)
    plt.close()

    np.savetxt('5-adc-measure/DATA.txt', measure, fmt='%d')
    np.savetxt('5-adc-measure/TIME.txt', timeline, fmt='%d')

################################################################################
# "Finally block" with functions that must be execute after script any way
################################################################################

finally:
    GPIO.cleanup()
    print('GPIO cleanup completed.')