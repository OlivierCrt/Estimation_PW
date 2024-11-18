import numpy as np

from simulationDonnees import *

# Configuration
N = 1000  # Nombre d'expériences aléatoires
sigma = 0.05  # Valeur de sigma pour le cas d'étude 1
cas_d_etude = 1
plot_p = False  # Désactiver l'affichage pour collecter les échantillons plus rapidement

# Stockage des réalisations de Z
realizations = []

for _ in range(N):
    Z, L, m, H, Hfull, bar_v, C_v, x = simulation_donnees(cas_d_etude, plot_p)
    realizations.append(Z)

# Convertir la liste en tableau NumPy pour analyses statistiques
realizations = np.array(realizations)

# Afficher les dimensions du tableau pour validation
print(f"Nombre de realisations collectees : {realizations.shape[0]}")
print(f"Dimensions d'une realisation Z : {realizations.shape[1]}")

# Calculer la moyenne et la covariance empirique des réalisations
mean_Z = np.mean(realizations, axis=0)
cov_Z = np.cov(realizations, rowvar=False)

# Afficher les résultats
print("Moyenne empirique de Z :")
print(mean_Z)
print("\nMatrice de covariance empirique de Z :")
print(cov_Z)

# Vérification des hypothèses
expected_cov = sigma**2 * np.eye(2 * L)
print("\nDifférence entre la covariance empirique et la covariance attendue :")
print(cov_Z - expected_cov)
