import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

data = np.loadtxt('/home/pi/GET/9-blood/DATA.txt')

#забыла сохранить данные время 9-16
t = 0
N = 20
timeline = []

for i in range (len(data)):
    timeline.append(t)
    t += 1

#create plot area
plt.title('График давления')
plt.xlabel('Время, с')
plt.ylabel('Давление, Барр')

#create smoothed plot
new = np.convolve(data, np.ones((N,))/N, mode = 'valid')

#create polynom plot
poly = np.polyfit(timeline, data, 8)
poly_y = np.poly1d(poly)(timeline)

#find extremums
s = 0
index = []

for i in range(len(new)-10):
    if (new[i+1] - new[i]) / (timeline[i+1] - timeline[i]) < 0 and (new[i+2] - new[i+1]) / (timeline[i+2] - timeline[i+1]) >= 0:
        index.append(i)
        plt.scatter(timeline[i], data[i], color='orange', marker='o')
        s += 1

#create plot
plt.plot(timeline, poly_y)
plt.plot(new, color = 'black')
plt.show()