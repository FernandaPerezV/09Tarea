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
Nmc = 10000
pendientes = np.zeros(Nmc)
coefs_posicion = np.zeros(Nmc)
for i in range(Nmc):
    r = np.random.normal(0, 1, size=len(flujo_i))
    muestra_i = flujo_i + error_i * r
    muestra_z = flujo_z + error_z * r
    pendientes[i], coefs_posicion[i] = np.polyfit(muestra_i, muestra_z, 1)


# plot 1
fig1 = plt.figure(1)
fig1.clf()
plt.hist(coefs_posicion, bins=30)
plt.draw()
plt.show()

# plot 2
fig2 = plt.figure(2)
fig2.clf()
plt.hist(pendientes, bins=30)
plt.draw()
plt.show()

# plot 3
a, b = np.polyfit(flujo_i, flujo_z, 1)
x = np.linspace(-100,500,1000)
fig3 = plt.figure(3)
fig3.clf()
plt.errorbar(flujo_i, flujo_z, xerr=error_i, yerr=error_z, fmt="o",
                 label="bla")
plt.plot(x, a * x + b)
plt.plot()
plt.draw()
plt.show()




# calculando intervalo de confianza
pendientes_ord = np.sort(pendientes)
coefs_posicion_ord = np.sort(coefs_posicion)
limite_bajo_1 = pendientes_ord[int(Nmc * 0.03)]
limite_alto_1 = pendientes_ord[int(Nmc * 0.98)]
limite_bajo_2 = coefs_posicion_ord[int(Nmc * 0.03)]
limite_alto_2 = coefs_posicion_ord[int(Nmc * 0.98)]
print """El intervalo de confianza al
             95% para la pendiente es: [{}:{}]""".format(limite_bajo_1,
                                                         limite_alto_1)
print """El intervalo de confianza al
             95% para el coef de posicion es: [{}:{}]""".format(limite_bajo_2,
                                                                limite_alto_2)
