import time
import numpy as np
import scipy as sc
from scipy import signal
import matplotlib.pyplot as plt

#Load DATA from a file into a list

data = np.loadtxt('/home/pi/GET/9-blood/DATA.txt')
print(data)
print(len(data))

t=0
N=20
timeline = []
for i in range (len(data)):
    timeline.append(t)
    t += 1

print(len(timeline))

plt.plot(timeline, data)
plt.title('График давления')
plt.xlabel('Время, с')
plt.ylabel('Давление, Барр')

new = np.convolve(data, np.ones((N,))/N, mode='same')

#poly = np.polyfit(timeline,data,8)
#poly_y = np.poly1d(poly)(timeline)

s=0
index = []

for i in range(len(new)-10):
    if (new[i+1] - new[i]) / (timeline[i+1] - timeline[i]) < 0 and (new[i+2] - new[i+1]) / (timeline[i+2] - timeline[i+1]) >= 0:
        index.append(i)
        plt.scatter(timeline[i], data[i], color='orange', marker='o')
        s += 1
        #print(s)

#plt.plot(data, 'white')
#plt.plot(timeline,poly_y)
plt.plot(new, color = 'black')

plt.show()







