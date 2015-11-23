from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt

# importando los datos
file_path = os.path.join('data', 'SNIa.dat')
distancias = np.loadtxt(fname=file_path, usecols=(1,))
velocidades = np.loadtxt(fname=file_path, usecols=(2,))

# 1 / H0_1 = suma(vi*di) / suma(di)
numerador = 0
denominador = 0
for i in range(len(distancias)):
    numerador += velocidades[i] * distancias[i]
    denominador += distancias[i] * distancias[i]
H0_1 = (numerador / denominador)**-1
print H0_1

# 1 / H0_2 = suma(di^2) / suma(vi/di)
numerador_2 = 0
denominador_2 = 0
for i in range(len(distancias)):
    numerador_2 += velocidades[i] * velocidades[i]
    denominador_2 += velocidades[i] * distancias[i]
H0_2 = (numerador_2 / denominador_2)**-1
print H0_2

# buscando intervalo de confianza al 95
# simulacion bootstrap
np.random.seed(1234)
N = len(distancias)
Nboot = 500
values_1 = np.zeros(Nboot)
values_2 = np.zeros(Nboot)
values_promedio = np.zeros(Nboot)

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
    values_1[i] = np.mean((num_1 / den_1)**-1)
    values_2[i] = np.mean((num_2 / den_2)**-1)
    values_promedio[i] = (values_1[i] + values_2[i]) * 0.5

values_ord = np.sort(values_promedio)
limite_bajo = values_ord[int(Nboot * 0.025)]
limite_alto = values_ord[int(Nboot * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo,
                                                            limite_alto)


# plot 1
fig = plt.figure(1)
fig.clf()
plt.hist(values_promedio, bins=50, facecolor='g', alpha=0.5)
plt.axvline((H0_1+H0_2)*0.5, color='r', label="Mejor valor encontrado")
plt.axvline(limite_bajo, color='b',
            label="Extremos intervalo de confianza al 95$\%$")
plt.axvline(limite_alto, color='b')
plt.title("Histograma $H_0$")
plt.legend(fontsize=11)
plt.ylim(0, 32)
plt.draw()
plt.show()
plt.savefig('bootstrap_p2.png')

print (H0_1+H0_2) * 0.5
