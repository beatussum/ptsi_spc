#! /usr/bin/env python3


from math import log10
import matplotlib.pyplot as plt
import numpy

ez_fe = 0.77 # en volt
ez_ce = 1.74 # en volt

def e(x: float) -> float:
    if x == 0:
        return None
    elif x < 1:
        return ez_fe + 0.06 * log10(( 1 / ( 1 - x ) ) - 1)
    elif x > 1:
        return ez_ce + 0.06 * log10(x - 1)
    else:
        return ( ez_fe + ez_ce ) / 2

plt.figure("Évolution théorique du potentiel de l'électrode en fonction de X.")

x_list = numpy.linspace(0, 3, 1_000)
plt.plot(x_list, numpy.vectorize(e)(x_list), "r", label = "$ E_{pt} = f(X) $")

plt.title("Évolution théorique de $ E_{pt} $ en fonction de $ X $.")
plt.grid()
plt.legend()
plt.xlabel("$ X $")
plt.ylabel("$ E_{pt} $")

plt.show()
