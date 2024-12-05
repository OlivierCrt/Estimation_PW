import numpy as np
import matplotlib.pyplot as plt

def simulation_donnees(cas_d_etude, plot_p):
    """
    Simulation d'une expérience.
    
    Arguments:
    cas_d_etude -- index de la section considérée dans le sujet
    plot_p -- si égal à 1, produit un affichage, sinon rien
    
    Retours:
    Z -- réalisation de la variable aléatoire de mesure (2Lx1)
    L -- nombre d'amers 2D
    m -- vecteur des positions des amers (2Lx1)
    H, Hfull -- matrices potentiellement utiles
    bar_v, C_v -- espérance et covariance du bruit de mesure additif Gaussien (2Lx1, 2Lx2L)
    x -- vecteur de paramètres caché (2x1)
    """
    L = 5  # Nombre d'amers
    x = np.array([2, 1])  # Ground truth
    m = np.array([5, -2, 3, 4, 0, 6, -2, 2, -1, -7])  # Positions des amers
    H = np.eye(2)
    Hfull = np.tile(H, (L, 1))

    if cas_d_etude == 1:
        sigma = 0.05  # 3sigma = 15cm
        bar_v = np.zeros(2 * L)
        C_v = (sigma**2) * np.eye(2 * L)
        Z = m - Hfull @ x + bar_v + np.linalg.cholesky(C_v).T @ np.random.randn(2 * L)
    elif cas_d_etude == 2:
        bar_v = np.zeros(2 * L)
        C_v = np.zeros((2 * L, 2 * L))
        for i in range(L):
            v_i = np.diag([0.07**2, 0.02**2])
            angle = (i) * np.pi / 6
            V_i = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            C_v[2 * i:2 * i + 2, 2 * i:2 * i + 2] = V_i @ v_i @ V_i.T
        Z = m - Hfull @ x + bar_v + np.linalg.cholesky(C_v).T @ np.random.randn(2 * L)
    elif cas_d_etude == 0:
        bar_v = np.zeros(2 * L)
        C_v = np.zeros((2 * L, 2 * L))
        tol = 1e-6
        for i in range(2 * L):
            vi = np.random.randn(2 * L)
            for j in range(i):
                vi -= np.dot(C_v[:, j], vi) * C_v[:, j]
            norm_vi = np.linalg.norm(vi)
            if norm_vi > tol:
                C_v[:, i] = vi / norm_vi
        v_diag = np.diag([0.001, 0.02])**2
        v = v_diag
        for i in range(2, L + 1):
            v = np.block([[v, np.zeros((v.shape[0], v_diag.shape[1]))],
                          [np.zeros((v_diag.shape[0], v.shape[1])), (i * v_diag)]])
        C_v = C_v @ v @ C_v.T
        Z = m - Hfull @ x + bar_v + np.linalg.cholesky(C_v).T @ np.random.randn(2 * L)
    elif cas_d_etude == 3:
        bar_v = np.zeros(2 * L)
        C_v = np.zeros((2 * L, 2 * L))
        for i in range(L):
            v_i = np.diag([0.02**2, 0.07**2])
            C_v[2 * i:2 * i + 2, 2 * i:2 * i + 2] = v_i
        Z = bar_v + np.linalg.cholesky(C_v).T @ np.random.randn(2 * L)
        for i in range(L):
            dx, dy = m[2 * i] - x[0], m[2 * i + 1] - x[1]
            r = dx + 1j * dy
            Z[2 * i] += abs(r)
            Z[2 * i + 1] += np.angle(r)
    else:
        print(f"Argument cas_d_etude erroné. Valeur : {cas_d_etude}")
        return None

    if plot_p:
        plt.figure()
        plt.axis([-6, 10, -8, 8])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True)
        plt.plot(x[0], x[1], 'r+', label='Robot')  # Robot
        for i in range(0, 2 * L, 2):
            plt.plot(m[i], m[i + 1], 'bo', label='Amers')  # Amers
        plt.title('+ : Robot --- o : Amers')
        plt.legend()
        plt.show()

    return Z, L, m, H, Hfull, bar_v, C_v, x



def ellipse(mx, Px, color='blue', confidence=0.99):
    """
    Trace une ellipse contenant un certain pourcentage des réalisations
    d'une variable aléatoire Gaussienne bivariée.
    
    Arguments :
        mx : np.ndarray
            Moyenne (vecteur 2x1).
        Px : np.ndarray
            Matrice de covariance (2x2).
        color : str
            Couleur de l'ellipse.
        confidence : float
            Niveau de confiance (par défaut 0.99, soit 99%).
    
    Retour :
        h : matplotlib.patches.Ellipse
            L'objet ellipse pour un usage ultérieur.
    """
    from matplotlib.patches import Ellipse
    import scipy.stats as stats

    # Calcul de la valeur chi² pour le niveau de confiance souhaité
    chi2_val = stats.chi2.ppf(confidence, df=2)

    # Décomposition en valeurs propres pour orienter l'ellipse
    eigvals, eigvecs = np.linalg.eigh(Px)
    
    # Rayon de l'ellipse (axe principal et secondaire)
    axes_lengths = 2 * np.sqrt(chi2_val * eigvals)  # Facteur 2 pour un diamètre
    
    # Angle d'orientation de l'ellipse
    angle = np.degrees(np.arctan2(eigvecs[1, 0], eigvecs[0, 0]))
    
    # Tracer l'ellipse avec matplotlib
    ellipse_patch = Ellipse(
        xy=mx,  # Centre de l'ellipse
        width=axes_lengths[0],  # Diamètre de l'axe principal
        height=axes_lengths[1],  # Diamètre de l'axe secondaire
        angle=angle,  # Orientation de l'ellipse
        edgecolor=color,
        facecolor='none',  # Transparent à l'intérieur
        linewidth=2
    )
    plt.gca().add_patch(ellipse_patch)
    
    # Retourner l'objet ellipse pour un usage supplémentaire
    return ellipse_patch
