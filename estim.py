import numpy as np
import matplotlib.pyplot as plt
from simulationDonnees import *

N = 1000  # Nombre d'expériences aléatoires
sigma = 0.05  # Valeur de sigma pour le cas d'étude 1
cas_d_etude = 1
plot_p = False  # Désactiver l'affichage pour collecter les échantillons rapidement

realizations = []

for _ in range(N):
    Z, L, m, H, Hfull, bar_v, C_v, x = simulation_donnees(cas_d_etude, plot_p)
    realizations.append(Z)
realizations = np.array(realizations)
print (realizations[0])

# Calculer la moyenne empirique des réalisations
mean_Z = np.mean(realizations, axis=0)

# Dimensions des données
L = len(m) // 2  # Nombre d'amers
x_indices = np.arange(0, 2 * L, 2)
y_indices = np.arange(1, 2 * L, 2)

plt.figure(figsize=(10, 8))

for i in range(N):
    plt.scatter(realizations[i, x_indices], realizations[i, y_indices], color='blue', alpha=0.05, s=5)
# Tracer la moyenne empirique
#plt.scatter(mean_Z[x_indices], mean_Z[y_indices], color='red', label='Moyenne empirique', s=50)


plt.xlabel("Coordonnée x")
plt.ylabel("Coordonnée y")
plt.title(f"{N} réalisations des observations Z")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()



plt.figure(figsize=(8, 6))


estime_vect = 1/N 