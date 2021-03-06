'''
Este script lee los datos del archivo hubble_original.dat y calcula la
constante H0 de Hubble de los maneras: 1) v=H*d 2) v/H=D. Luego utiliza
el metodo de biseccion para mezclar ambas soluciones.
Realiza una simulacion de bootstrap para calcular el intervalo de
confianza al 95%.
Realiza 2 plots:
1) Datos + 3 rectas (con los 2 H calculados y en H_biseccion como pendientes)
2) Histograma para H0.
'''
from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt


def biseccion(a1, a2):
    return (a1 * a2 - 1 + np.sqrt((1+a1**2) * (1+a2**2))) / (a1+a2)


# importando los datos
file_path = os.path.join('data', 'hubble_original.dat')
distancias = np.loadtxt(fname=file_path, usecols=(0,))
velocidades = np.loadtxt(fname=file_path, usecols=(1,))

# H0_1 = suma(vi*di) / suma(di)
numerador = 0
denominador = 0
for i in range(len(distancias)):
    numerador += velocidades[i] * distancias[i]
    denominador += distancias[i] * distancias[i]
H0_1 = numerador / denominador
print H0_1

# H0_2 = suma(vi^2) / suma(vi*di)
numerador_2 = 0
denominador_2 = 0
for i in range(len(distancias)):
    numerador_2 += velocidades[i] * velocidades[i]
    denominador_2 += velocidades[i] * distancias[i]
H0_2 = numerador_2 / denominador_2
print H0_2


# buscando intervalo de confianza al 95
# simulacion bootstrap
np.random.seed(1234)
N = len(distancias)
Nboot = 500
values_bis = np.zeros(Nboot)

for i in range(Nboot):
    s = np.random.randint(low=0, high=N, size=N)
    num_1 = 0
    den_1 = 0
    num_2 = 0
    den_2 = 0
    for j in s:
        num_1 += velocidades[j] * distancias[j]
        den_1 += distancias[j] * distancias[j]
        num_2 += velocidades[j] * velocidades[j]
        den_2 += velocidades[j] * distancias[j]
    values_1 = np.mean(num_1 / den_1)
    values_2 = np.mean(num_2 / den_2)
    values_bis[i] = biseccion(values_1, values_2)

values_ord = np.sort(values_bis)
limite_bajo = values_ord[int(Nboot * 0.025)]
limite_alto = values_ord[int(Nboot * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo,
                                                            limite_alto)
# plot 1
x = np.linspace(0, 2, 100)
fig1 = plt.figure(1)
fig1.clf()
plt.plot(distancias, velocidades, 'o', label="Datos")
plt.plot(x, x*H0_1, color='r', label="Caso 1")
plt.plot(x, x*H0_2, color='g', label="Caso 2")
plt.plot(x, x*np.mean(values_bis), color='y', label="Biseccion")
plt.legend(loc=2)
plt.xlabel("Distancias [Mpc]")
plt.ylabel("Velocidades [km / s]")
plt.draw()
plt.show()
plt.savefig('datos_y_rectas_p1.png')


# plot 2
fig2 = plt.figure(1)
fig2.clf()
plt.hist(values_bis, bins=50, facecolor='g', alpha=0.5)
plt.axvline(biseccion(H0_1, H0_2), color='r', label="Mejor valor encontrado")
plt.axvline(limite_bajo, color='b',
            label="Extremos intervalo de confianza al 95$\%$")
plt.axvline(limite_alto, color='b')
plt.title("Histograma $H_0$")
plt.legend(fontsize=11)
plt.ylim(0, 50)
plt.draw()
plt.show()
plt.savefig('histograma_p1.png')
