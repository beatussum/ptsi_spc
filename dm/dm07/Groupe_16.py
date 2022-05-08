#! /usr/bin/env python3


import matplotlib.pyplot as plt
import numpy
import scipy.optimize

## Données

n = 1      # en mole
r = 8.13   # en u.s.i.
t = 298.15 # en kelvin

pc = 506_625 # en pascal
tc = 217.15  # en kelvin

a = ( 27 * ( r * tc )**2 ) / ( 64 * pc )
b = ( r * tc ) / ( 8 * pc )

vi = 1e-7 # en mètre cube
vf = 1    # en mètre cube
e  = 1e-7 # en mètre cube

## Question 2

def v_gaz_parfait(p: float) -> float:
    return ( n * r * t ) / p

def f(p: float, v: float) -> float:
    return p * v**3 - n * ( b * p + r * t ) * v**2 + a * n**2 * v \
        - a * b * n**3

def Dichotomie(p: float, vi: float, vf: float, e: float) -> float:
    while vi <= vf:
        c  = ( vi + vf ) / 2
        fc = f(p, c)

        if abs(fc) <= e:
            return c
        elif ( fc * f(p, vf) ) < 0:
            vi = c
        else:
            vf = c

    return -1.0

print("""
==== Question 2 ====

""")

for p in [1, 500]:
    vparfait = v_gaz_parfait(p * 1e5)
    vreel    = Dichotomie(p * 1e5, vi, vf, e)

    diff = abs(vparfait - vreel)

    print(
        f"Pour P = {p} bar, on observe une différence de {diff:.3e} mètres " +
        "cubes entre les deux modèles."
    )

## Question 3

def Pression_reduite(tr: float, vr: float) -> float:
    return ( ( 8 * tr ) / ( 3 * vr - 1 ) ) - ( 3 / vr**2 )

listeTr = [0.7, 0.85, 1, 1.5]
listeVr = numpy.linspace(0.4, 15, 1_000)
listey  = [ numpy.vectorize(Pression_reduite)(tr, listeVr) for tr in listeTr ]

plt.figure(
    "Réseau d'isothermes d'Andrews\n" +
    "(en diagramme de Clapeyron réduit)"
)

for (tr, y) in zip(listeTr, listey):
    plt.plot(listeVr, y, label = f"isotherme pour $ T_r = {tr} $")

plt.title(
    "Réseau d'isothermes d'Andrews\n" +
    "(en diagramme de Clapeyron réduit)"
)

plt.xlabel("$ V_r $ (sans unité)")
plt.ylabel("$ P_r $ (sans unité)")
plt.xlim(0, 15)
plt.ylim(-1.5, 10)
plt.grid()
plt.legend()

plt.show()

## Question 4

def Minimum(listePr: list[float]) -> int:
    m, min_val = 0, listePr[0]

    for (i, pr) in enumerate(listePr[1:], 1):
        if pr < min_val:
            m, min_val = i, pr
        else:
            """
            Nécessaire dans le cas où la pression réduite tend en l'infini vers
            une valeur inférieure à celle du minimum local.
            """
            break

    return m

def Extremum(listePr: list[float]) -> tuple[int, int, list[float]]:
    m          = Minimum(listePr)
    M, max_val = m, listePr[m]

    for (i, pr) in enumerate(listePr[m + 1:], m + 1):
        if pr > max_val:
            M, max_val = i, pr

    return m, M, listePr[m:M + 1]

def Rectangle(
    i: float,
    j: float,
    Pr_sat_inconnue: float,
    Tr: float,
    n: int
) -> float:

    ret = 0

    for k in range(n):
        ret += ( Pression_reduite(Tr, i + k * ( ( j - i ) / n )) \
            - Pr_sat_inconnue )

    ret *= ( j - i ) / n

    return ret

def Palier(
    Tr: float,
    listeVr: list[float],
    listePr: list[float]
) -> tuple[float, float, float]:

    m, M, _ = Extremum(listePr)

    Vrf = None
    Vrb = None

    def f(Pr: float) -> float:
        nonlocal Vrf, Vrb

        g = lambda Vr: Pression_reduite(Tr, Vr) - Pr

        Vrf = scipy.optimize.bisect(g, listeVr[0], listeVr[m])

        """
        On vérifie qu'il existe bien une racine `B` pour la valeur
        `Pr_sat_inconnue` = `Pr` ; sinon, on prend la dernière valeur de
        `listeVr` comme borne supérieure pour le calcul de l'aire.
        """
        try:
            Vrb = scipy.optimize.bisect(g, listeVr[M], listeVr[-1])
        except ValueError:
            Vrb = listeVr[-1]

        return Rectangle(Vrf, Vrb, Pr, Tr, 100)

    palier = scipy.optimize.bisect(f, listePr[m], listePr[M])

    return palier, Vrf, Vrb

def generer_reseau_isotherme(listeTr: float) -> list[list[float]]:

    listey = [ numpy.vectorize(Pression_reduite)(tr, listeVr) for tr in listeTr ]
    ret    = []

    for (tr, y) in zip(listeTr, listey):
        palier, Vrf, Vrb = Palier(tr, listeVr, y)

        z = []

        for (vr, pr) in zip(listeVr, y):
            if Vrf < vr < Vrb:
                z.append(palier)
            else:
                z.append(pr)

        ret.append(z)

    return ret

"""
L'utilisation de `numpy.arange` engendre des problèmes liés à la représentation
des flotants par la norme IEEE 754.
"""
listeTr2 = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

plt.figure(
    "Réseau d'isothermes d'Andrews\n" +
    "(en diagramme de Clapeyron réduit)"
)

for (tr, y) in zip(listeTr2, generer_reseau_isotherme(listeTr2)):
    plt.plot(listeVr, y, label = f"isotherme pour $ T_r = {tr} $")

plt.title(
    "Réseau d'isothermes d'Andrews\n" +
    "(en diagramme de Clapeyron réduit)"
)

plt.xlabel("$ V_r $ (sans unité)")
plt.ylabel("$ P_r $ (sans unité)")
plt.xlim(0, 5)
plt.ylim(-1.0, 2.0)
plt.grid()
plt.legend()

plt.show()

### Question 4.f

def generer_courbe_saturation(
    listeTr: list[float]
) -> tuple[list[float], list[float]]:

    listey = [ numpy.vectorize(Pression_reduite)(tr, listeVr) for tr in listeTr ]
    z      = []

    for (tr, y) in zip(listeTr, listey):
        palier, Vrf, Vrb = Palier(tr, listeVr, y)

        z += [[Vrf, palier], [Vrb, palier]]

    """
    On trie la liste par abscisse croissante.
    """
    z.sort(key = lambda a: a[0])

    return numpy.transpose(z)

plt.figure(
    "Courbe de saturation\n" +
    "(en diagramme de Clapeyron réduit)"
)

listeTr3 = numpy.linspace(0.7, 1.0, 100)
x, y     = generer_courbe_saturation(listeTr3)

plt.plot(x, y, "k--", label = "Courbe de saturation")

plt.title(
    "Courbe de saturation\n" +
    "(en diagramme de Clapeyron réduit)"
)

plt.xlabel("$ V_r $ (sans unité)")
plt.ylabel("$ P_r $ (sans unité)")
plt.xlim(0, 15)
plt.ylim(-1.5, 10)
plt.grid()
plt.legend()

plt.show()

### Question 4.g

plt.figure(
    "Réseau d'isothermes d'Andrews avec courbe de saturation\n" +
    "(en diagramme de Clapeyron réduit)"
)

for (tr, y) in zip(listeTr2, generer_reseau_isotherme(listeTr2)):
    plt.plot(listeVr, y, label = f"isotherme pour $ T_r = {tr} $")

x, y = generer_courbe_saturation(listeTr3)

plt.plot(x, y, "k--", label = "Courbe de saturation")

plt.title(
    "Réseau d'isothermes d'Andrews avec courbe de saturation\n" +
    "(en diagramme de Clapeyron réduit)"
)

plt.xlabel("$ V_r $ (sans unité)")
plt.ylabel("$ P_r $ (sans unité)")
plt.xlim(0, 5)
plt.ylim(-1.0, 2.0)
plt.grid()
plt.legend()

plt.show()
