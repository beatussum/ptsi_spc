#! /usr/bin/env python3


from math import pi
import matplotlib.pyplot as plt
import numpy

"""
Lecture et récupération des valeurs de la vitesse adimensionnée depuis un
fichier.
"""

def read_file(file_name):
    content = numpy.loadtxt(file_name)

    return (content[:, 0] - content[0, 0], content[:, 1] - content[0, 1])

times, vadim = read_file("vadim.txt")

"""
Données.
"""

g = 9.8 # en mètre par seconde carrée

m = 32e-3   # en kilogramme
r = 12.5e-3 # en mètre

vlim = 1.581     # en mètre par seconde
tau  = 1 / 2.745 # en seconde
 
"""
Création du premier graphe.
"""

plt.figure(0)
plt.title("Évolution de la vitesse adimensionnée en fonction du temps")
plt.plot(times, vadim, "b", label = "résultats expérimentaux")
plt.plot(times, times / tau, "k", label = "tangente à l'origine")
plt.xlabel("temps (en seconde)")
plt.ylabel(r"$ v^* $ (en mètre par seconde)")
plt.xlim(0, times[-1])
plt.grid()
plt.legend()

"""
Calcul et affichage des masses volumiques des corps étudiés.
"""

vb   = (4 / 3) * pi * r**3
rhob = m / vb
rho  = rhob * ( 1 - ( vlim / ( g * tau ) ) )

print(f"La bille a pour masse volumique {rhob:.1e} kilogramme par mètre cube.")
print(f"Le fluide étudié a pour masse volumique {rho:.1e} kilogramme par mètre cube.")

"""
Implémentation de la résolution par la méthode d'Euler.
"""

def f(y, a):
    return ( 1 - y**a ) / tau

def euler(f, xzero, last_time, step, **kwargs):
    ret = { 0: xzero }

    t = 0
    while t <= last_time:
        ret[t + step] = step * f(ret[t], **kwargs) + ret[t]
        t += step
    
    return (ret.keys(), ret.values())

"""
Création du deuxième graphe.
"""

plt.figure(1)

plt.title(
    "Évolution de la vitesse adimensionnée en fonction du temps et\n"
    "détermination de la loi de forces"
)

my_euler = lambda a: euler(f, 0, times[-1], 1e-3, a = a)

plt.plot(times, vadim, "r+", label = "résultats expérimentaux")
plt.plot(*my_euler(1), "b", label = "a = 1")
plt.plot(*my_euler(2), "g", label = "a = 2")

plt.xlabel("temps (en seconde)")
plt.ylabel(r"$ v^* $ (en mètre par seconde)")
plt.xlim(0, times[-1])
plt.grid()
plt.legend()

"""
Calcul et affichage du coefficient de frottements.
"""

a     = 2
gamma = rho / rhob
k     = m * g * ( 1 - gamma ) / vlim**a

print(f"Le coefficient de frottements vaut {k:.1e} kilogramme par mètre.")

"""
On affiche les deux graphes en même temps.
"""

plt.show()