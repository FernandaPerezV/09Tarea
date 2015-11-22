from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt

# importando flujos y errores
file_path = os.path.join('data', 'DR9Q.dat')
flujo_i = np.loadtxt(fname=file_path, usecols=(79,)) * 3.631
error_i = np.loadtxt(fname=file_path, usecols=(80,)) * 3.631
flujo_j = np.loadtxt(fname=file_path, usecols=(81,)) * 3.631
error_j = np.loadtxt(fname=file_path, usecols=(82,)) * 3.631
