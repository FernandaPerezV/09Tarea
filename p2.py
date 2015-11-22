from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt

# importando los datos
file_path = os.path.join('data', 'SNIa.dat')
distancias = np.loadtxt(fname=file_path, usecols=(1,))
velocidades = np.loadtxt(fname=file_path, usecols=(2,))

# H0 = suma(vi*di) / suma(di)
numerador = 0
denominador = 0
for i in range(len(distancias)):
    numerador += velocidades[i] * distancias[i]
    denominador += distancias[i] * distancias[i]
H0 = (numerador / denominador)**-1
print H0

# buscando intervalo de confianza al 95
# simulacion bootstrap
np.random.seed(1234)
N = len(distancias)
Nboot = 500
values = np.zeros(Nboot)

for i in range(Nboot):
    s = np.random.randint(low=0, high=N, size=N)
    num = 0
    den = 0
    for j in s:
        num += velocidades[j] * distancias[j]
        den += distancias[j] * distancias[j]
    values[i] = np.mean((num / den)**-1)

values_ordenados = np.sort(values)
limite_bajo = values_ordenados[int(Nboot * 0.03)]
limite_alto = values_ordenados[int(Nboot * 0.98)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo, limite_alto)

# plot
fig = plt.figure(1)
fig.clf()
plt.hist(values, bins=50)
plt.axvline(H0, color='r')
plt.draw()
plt.show()
plt.savefig('bootstrap_p2.png')
