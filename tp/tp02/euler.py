#! /usr/bin/env python3


from math import sqrt
import matplotlib.pyplot as plt

"""
Implémentation de la méthode d'Euler
"""

def f(z, y, q, wz):
    return - ( wz / q ) * z - wz**2 * y

def euler(f, zz, yz, end, h, q, wz):
    times   = [0]
    yvalues = [yz]
    z       = zz

    while times[-1] < end:
        times.append(times[-1] + h)
        z += h * f(z, yvalues[-1], q, wz)
        yvalues.append(yvalues[-1] + h * z)

    return (times, yvalues)

"""
Test
"""

c  = 10e-9 # en farad
l  = 47e-3 # en henry
r  = 0     # en ohm
rg = 50    # en ohm

plt.title("Tracé des trois régimes transitoires")

wz = 1 / sqrt(l * c)

for rv in [1e3, 4.3e3, 1e4]:
    req = r + rg + rv
    q   = (wz * l ) / req

    times, values = euler(f, 0, 5, 0.6e-3, 1e-6, q, wz)

    plt.plot(times, values, label = f"q = {q:.1e}")

plt.xlabel("temps (en seconde)")
plt.ylabel("$ u_c $ (en volt)")
plt.legend()
plt.grid()

plt.show()