import time
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

data = np.loadtxt('/home/pi/Repositories/get/9-blood/Data/DATA.txt')
timeline = np.loadtxt('/home/pi/Repositories/get/9-blood/Data/TIME.txt')

#data of pressure and puls from keyboard
#SP = (int(input('Systolic pressure: ')))
#DP = (int(input('Diastolic pressure: ')))
#num = (int(input('Number of beats: ')))
SP = 118
DP = 59
num = 11

#time of pressure for calculations of puls
for i in range(len(data)):
    if data[i] == SP:
        tSP = timeline[i]      
    if data[i] == DP:
        tDP = timeline[i]

puls = 60 / (tDP - tSP) * num
print(round(puls))

#create data of smoothed plot
N = 100
new = np.convolve(data, np.ones((N,))/N, mode = 'valid')

#delete timeline elements
for i in range (N-1):
    timeline = np.delete(timeline, 0)

#CREATE PLOT AREA
fig = plt.figure()
ax = fig.add_subplot(111)

ax.set(title = 'График зависимости P(t)',
        xlabel = 'Время, с',
        ylabel = 'Давление, мм.рт.ст.')

ax.grid(which='major',
        color = 'k')
            
ax.grid(which='minor',
        color = 'gray',
        inestyle = ':')

#create smoothed plot
ax.plot(timeline, new)

ax.scatter(tSP, SP, color = 'red', marker='.')
ax.scatter(tDP, DP, color = 'red', marker='.')

ax.text(tSP + 0.5, SP, 'SP = {}'.format(SP))
ax.text(tDP + 0.5, DP, 'DP = {}'.format(DP))

plt.show()

plt.savefig('/home/pi/Repositories/get/9-blood/Data/Smoothed_plot_{}-{}.png'.format(SP, DP))