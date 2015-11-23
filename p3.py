from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats


# importando flujos y errores
file_path = os.path.join('data', 'DR9Q.dat')
flujo_i = np.loadtxt(fname=file_path, usecols=(80,)) * 3.631
error_i = np.loadtxt(fname=file_path, usecols=(81,)) * 3.631
flujo_z = np.loadtxt(fname=file_path, usecols=(82,)) * 3.631
error_z = np.loadtxt(fname=file_path, usecols=(83,)) * 3.631

# montecarlo
np.random.seed(1234)
Nmc = 100
mean_values_i = np.zeros(Nmc)
mean_values_z = np.zeros(Nmc)
for i in range(Nmc):
    r = np.random.normal(0, 1, size=len(flujo_i))
    muestra_i = flujo_i + error_i * r
    mean_values_i[i] = np.mean(muestra_i)
    muestra_z = flujo_z + error_z * r
    mean_values_z[i] = np.mean(muestra_z)

[a, b] = np.polyfit(mean_values_i, mean_values_z, 1)
[c, d] = np.polyfit(flujo_i, flujo_z, 1)
#x = np.linspace(0,450,1000)

fig = plt.figure(1)
fig.clf()
plt.plot(flujo_i, flujo_z, 'o')
plt.errorbar(flujo_i, flujo_z, yerr=error_z, xerr=error_i,
             marker='.', ls='None', capsize=0.,color='g')
#plt.plot(x, b + a * x)
#plt.plot(x, d + c * x)
plt.draw()
plt.show()

'''
fig2 = plt.figure(2)
fig2.clf()
plt.hist(mean_values_i/mean_values_z, bins=30)
#plt.axvline(b, color='r')
plt.draw()
plt.show()
'''
