import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

data = np.loadtxt('/home/pi/GET/9-blood/DATA.txt')
#time = np.loadtxt('/home/pi/GET/9-blood/TIME.txt')
data.astype(np.int32)

#забыла сохранить данные время 9-16
t = 0
N = 20
timeline = []

for i in range (len(data)):
    timeline.append(t)
    t += 1

#data of pressure and puls from keyboard
#SP = (int(input('Systolic pressure: ')))
#DP = (int(input('Diastolic pressure: ')))
#num = (int(input('Number of beats: ')))
SP = 103
DP = 57
num = 6

#time of pressure for calculations of puls
for i in range(len(data)):
    if data[i] == SP:
        tSP = timeline[i]       
    if data[i] == DP:
        tDP = timeline[i]

puls = 60 / (tDP - tSP) * num
print(puls)

# create plot area
plt.title('График давления')
plt.xlabel('Время, с')
plt.ylabel('Давление, Барр')

#create smoothed plot
new = np.convolve(data, np.ones((N,))/N, mode = 'valid')

plt.plot(new) 
plt.plot(data) 
plt.scatter(tSP, SP, color = 'blue', marker='o')
plt.scatter(tDP, DP, color = 'blue', marker='o')
plt.show()