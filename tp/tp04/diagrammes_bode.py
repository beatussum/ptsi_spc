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

filename = "data.txt"
e        = 5      # en volt
fz       = 1.00e3 # en hertz

"""
Fonction de transfert.
"""

def h(f: float) -> complex:
    return 1 / complex(1, f / fz)

"""
Calcule les valeurs théoriques en gain et en amplitude pour un intervalle de
fréquence données.
"""

def compute_th_values(flist: Sequence[float]) -> ndarray_triplet:
    gains   = []
    philist = []

    for f in flist:
        hv = h(f)

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
    # Récupération des valeurs expérimentales et théoriques.
    flist, expgains, expphi = read_exp_values(filename)
    _, thgains, thphi       = compute_th_values(flist)

    plt.figure("Diagrammes de Bode d'un filtre passe-bas du premier ordre")
    plt.suptitle("Diagrammes de Bode d'un filtre passe-bas du premier ordre")

    # Création du diagramme de Bode en amplitude.
    gplot = plt.subplot(211)

    # Création des graphes réels.
    plt.semilogx(flist, expgains, "+-r", mec = "k", label = "expérience")
    plt.semilogx(flist, thgains, "k", label = "théorie")

    # Création des graphes asymptotiques.
    plt.hlines(thgains[0], flist[0], fz)
    f = numpy.linspace(fz, flist[-1])
    plt.semilogx(f, - 20 * numpy.log10(f / fz) + thgains[0])

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

    # Création des graphes asymptotiques.
    plt.hlines(thphi[0], flist[0], fz)
    plt.vlines(fz, thphi[0], thphi[-1])
    plt.hlines(thphi[-1], fz, flist[-1])

    plt.title("Diagramme de Bode en phase")
    plt.xlabel("Fréquence (en hertz)")
    plt.ylabel("Phase (en radian)")
    plt.xlim(flist[0], flist[-1])
    plt.grid(which = "both")
    plt.legend()

    plt.show()

show_plot()
