import numpy as np
import matplotlib.pyplot as plt
import os

# importando los datos
file_path = os.path.join('data', 'hubble_original.dat')
distancias = np.loadtxt(fname=file_path, usecols=(0,))
velocidades = np.loadtxt(fname=file_path, usecols=(1,))

fig = plt.figure(1)
fig.clf()

ax = fig.add_subplot(111)
ax.set_xlabel('Distancia [$Mpc$]')
ax.set_ylabel('Velocidad [$km/s$]')
plt.title("Datos originales Hubble")
plt.plot(distancias, velocidades, 'o')
plt.draw()
plt.show()
