'''
Este script lee los datos del archivo DR9Q.dat y calcula la recta que mejor
relaciona el flujo de la banda i con el de la banda z.
Realiza una simulacion de monte carlo para calcular el intervalo de
confianza al 95%.
Realiza 3 plots:
1) Datos + recta con ajuste lineal
2) Histograma para pendiente
3) Histograma para coeficiente de posicion
'''

from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats


def biseccion(I, Z):
    coef1 = np.polyfit(I, Z, 1)
    coef2 = np.polyfit(Z, I, 1)
    x_c = (coef1[1]*coef2[0]+coef2[1])/(1.0-coef1[0]*coef2[0])
    y_c = coef1[0]*x_c + coef1[1]
    m = np.tan((np.arctan(coef1[0]) + np.arctan(1.0/coef2[0])) / 2.0)
    return (m, y_c - m*x_c)


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
    f = biseccion(muestra_i, muestra_z)
    pendientes[i], coefs_posicion[i] = f[0], f[1]

a, b = biseccion(flujo_i, flujo_z)

# calculando intervalo de confianza
pendientes_ord = np.sort(pendientes)
coefs_posicion_ord = np.sort(coefs_posicion)
limite_bajo_1 = pendientes_ord[int(Nmc * 0.025)]
limite_alto_1 = pendientes_ord[int(Nmc * 0.975)]
limite_bajo_2 = coefs_posicion_ord[int(Nmc * 0.025)]
limite_alto_2 = coefs_posicion_ord[int(Nmc * 0.975)]
print """El intervalo de confianza al
      95% para la pendiente es: [{}:{}]""".format(limite_bajo_1,
                                                  limite_alto_1)
print """El intervalo de confianza al
      95% para el coef de posicion es: [{}:{}]""".format(limite_bajo_2,
                                                         limite_alto_2)

# plot 1
fig1 = plt.figure(1)
fig1.clf()
plt.hist(coefs_posicion, bins=30, facecolor='g', alpha=0.5)
plt.axvline(b, color='r', label="Valor encontrado con ajuste lineal")
plt.axvline(limite_bajo_2, color='b',
            label="Extremos intervalo de confianza al 95$\%$")
plt.axvline(limite_alto_2, color='b', linewidth=1)
plt.title('Histograma coeficientes de posicion')
plt.legend(fontsize=11)
plt.draw()
plt.show()
plt.savefig('histo_p3_1.png')

# plot 2
fig2 = plt.figure(2)
fig2.clf()
plt.hist(pendientes, bins=30, facecolor='g', alpha=0.5)
plt.axvline(a, color='r', label="Valor encontrado con ajuste lineal")
plt.axvline(limite_bajo_1, color='b',
            label="Extremos intervalo de confianza al 95$\%$")
plt.axvline(limite_alto_1, color='b')
plt.title('Histograma pendientes')
plt.ylim(0, 2700)
plt.legend(loc=2, fontsize=11)
plt.draw()
plt.show()
plt.savefig('histo_p3_2.png')

# plot 3
x = np.linspace(-100, 500, 1000)
fig3 = plt.figure(3)
fig3.clf()
plt.errorbar(flujo_i, flujo_z, xerr=error_i, yerr=error_z, fmt="o",
             label="Datos ", color='g', alpha=0.5)
plt.plot(x, a * x + b, color='r', label="Ajuste lineal")
plt.xlabel("Flujo banda i [$10^{-6}Jy$]")
plt.ylabel("Flujo banda z [$10^{-6}Jy$]")
plt.legend(loc=2)
plt.plot()
plt.draw()
plt.show()
plt.savefig('ajuste_p3.png')
