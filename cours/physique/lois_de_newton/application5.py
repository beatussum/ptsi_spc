#! /usr/bin/env python3


import matplotlib.pyplot as plt
import numpy
import scipy.integrate

"""
Données du sujet
"""

m    = 400 # g
g    = 9.8 # m s^{-2}
h    = 25  # m
beta = 40  # kg m^{-1}

"""
Conversion en unités S.I.
"""

m *= 1e-3

def a(v, t):
    return - g - ( beta / m ) * v**2

times = numpy.linspace(0, 100)
v     = scipy.integrate.odeint(a, 0, times)

plt.plot(times, v, "b", label="vitesse")
plt.legend()
plt.xlabel("temps")
plt.grid()
plt.show()
