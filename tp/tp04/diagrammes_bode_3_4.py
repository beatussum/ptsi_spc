#! /usr/bin/env python3


from collections.abc import Sequence
from cmath import phase
from math import log10
import matplotlib.pyplot as plt
import numpy

"""
Définitions de type.
"""

ndarray_triplet = tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]

"""
Données.
"""

filenames = ["data3.txt", "data4.txt"]

titles = [
    "mise en cascade de deux filtres du premier ordre",
    "mise en cascade avec suiveur"
]

e         = 5              # en volt
fz        = 1.00e3         # en hertz
qlist     = [1 / 3, 1 / 2] # sans unité

"""
Fonction de transfert.
"""

def h(f: float, q: float) -> complex:
    return complex(0, f / fz) / complex(1 - ( f / fz )**2, f / ( q * fz ))

"""
Calcule les valeurs théoriques en gain et en amplitude pour un intervalle de
fréquence données.
"""

def compute_th_values(flist: Sequence[float], q: float) -> ndarray_triplet:
    gains   = []
    philist = []

    for f in flist:
        hv = h(f, q)

        gains.append(20 * log10(abs(hv) * e))
        philist.append(phase(hv))

    return (flist, gains, philist)

"""
Récupère les valeurs expérimentales stockées dans un fichier.
"""

def read_exp_values(filename: str) -> ndarray_triplet:
    flist, ulist, philist = numpy.loadtxt(
        filename,
        delimiter = "\t",
        unpack = True
    )

    return (flist, 20 * numpy.log10(ulist), philist)

"""
Affiche les diagrammes de Bode.
"""

def show_plot() -> None:
    for (f, q, t) in zip(filenames, qlist, titles):
        title = f"Diagrammes de Bode d'un filtre passe-bas du premier ordre\n({t})"

        # Récupération des valeurs expérimentales et théoriques.
        flist, expgains, expphi = read_exp_values(f)
        _, thgains, thphi       = compute_th_values(flist, q)

        plt.figure(title)
        plt.suptitle(title)

        # Création du diagramme de Bode en amplitude.
        gplot = plt.subplot(211)

        # Création des graphes réels.
        plt.semilogx(flist, expgains, "+-r", mec = "k", label = "expérience")
        plt.semilogx(flist, thgains, "k", label = "théorie")

        plt.title("Diagramme de Bode en amplitude")
        plt.ylabel("Amplitude (en décibel)")
        plt.grid(which = "both")
        plt.legend()
        plt.tick_params("x", labelbottom = False)

        # Création du diagramme de Bode en phase.
        plt.subplot(212, sharex = gplot)

        # Création des graphes réels.
        plt.semilogx(flist, expphi, "+-r", mec = "k", label = "expérience")
        plt.semilogx(flist, thphi, "k", label = "théorie")

        plt.title("Diagramme de Bode en phase")
        plt.xlabel("Fréquence (en hertz)")
        plt.ylabel("Phase (en radian)")
        plt.xlim(flist[0], flist[-1])
        plt.grid(which = "both")
        plt.legend()

    plt.show()

def test(q: float) -> None:
    for f in numpy.linspace(100, 50e3, 200):
        hv = h(f, q)

        print(f, abs(hv) * e, phase(hv), sep = "\t")

show_plot()