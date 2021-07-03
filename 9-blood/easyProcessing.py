import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

data = np.loadtxt('/home/pi/GET/9-blood/DATA.txt')
#time = np.loadtxt('/home/pi/GET/9-blood/TIME.txt')
#data.astype(np.int32)

#забыла сохранить данные время 9-16
t = 0
timeline = []

for i in range (len(data)):
    timeline.append(t)
    t += 1

#data of pressure and puls from keyboard
#SP = (int(input('Systolic pressure: ')))
#DP = (int(input('Diastolic pressure: ')))
#num = (int(input('Number of beats: ')))
SP = 116
DP = 57
num = 8


#sliding smoothing
N = 500
new = []
sum = 0

for i in range (len(data) - N):
    
    for k in range(N):
        sum += data[i]
 
    sr = sum / N
    new.append(sr)
    sr = 0
    sum = 0
print (new)


#time of pressure for calculations of puls
#for i in data:
    #if float(data[i]) == SP:
        #tSP = timeline[i]
    #if float(data[i]) == SP:
        #tDP = timeline[i]

#puls = N / (tDP - tSP)

# create plot area
plt.plot(new)
plt.title('График давления')
plt.xlabel('Время, с')
plt.ylabel('Давление, Барр')

#create plot
plt.plot(new, color = 'black') 
#plt.scatter(tSP, SP, color='orange', marker='o')
#plt.scatter(tDP, DP, color='orange', marker='o')

plt.show()