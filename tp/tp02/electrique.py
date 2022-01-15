#! /usr/bin/env python3


from math import log
import matplotlib.pyplot as plt
import numpy

def read_file(file_name):
    content = numpy.loadtxt(file_name)

    return (content[:, 0], content[:, 1])

def find_maxima(times, tension):
    maximum         = False
    maximum_index   = []
    maximum_times   = []
    maximum_tension = []

    for i in range(1, len(times)):
        if tension[i] > 4:
            continue

        if ( tension[i - 1] < tension[i] ) == maximum:
            maximum = not maximum

            if maximum:
                maximum_index.append(i)
                maximum_times.append(times[i])
                maximum_tension.append(tension[i])

    return (maximum_index, maximum_times, maximum_tension)

def compute_period(times, tension):
    _, maxima_times, _ = find_maxima(times, tension)

    return ( maxima_times[-1] - maxima_times[0] ) / ( len(maxima_times) - 1 )

def logarithmic_decrement(times, tension, period):
    first_period, *_, last_period = find_maxima(times, tension)[0]

    delta       = []
    tension_inf = tension[-1]

    def tension_at(t):
        for i in range(1, len(times)):
            if times[i] == t:
                return tension[i]
            elif times[i] > t:
                a = ( tension[i] - tension[i - 1] ) / ( times[i] - times[i - 1] )

                return a * ( t - times[i - 1] ) + tension[i - 1]

        return tension_inf

    for i in range(first_period, last_period + 1):
        d = ( tension[i] - tension_inf ) / ( tension_at(tension[i] + period) - tension_inf )
        delta.append(d)

    return log(numpy.average(d))

""" def logarithmic_decrement(times, tension, _):
    _, maximum_times, maximum_tension = find_maxima(times, tension)

    delta       = []
    tension_inf = tension[-1]

    for i in range(1, len(maximum_times)):
        d = ( maximum_tension[i - 1] - tension_inf ) / ( maximum_tension[i] - tension_inf )
        delta.append(d)

    return log(numpy.average(d)) """

"""
Traitement des données
"""

exp_times, exp_tensions = read_file("electrique.txt")

plt.figure(1)
plt.title(r"Évolution temporelle de $ u_c $")
plt.plot(exp_times, exp_tensions, "b")
plt.xlabel("temps (en seconde)")
plt.ylabel(r"$ u_c $ (en volt)")
plt.grid()

period = compute_period(exp_times, exp_tensions)
#delta  = logarithmic_decrement(exp_times, exp_tensions, period)

_, mt, _ = find_maxima(exp_times, exp_tensions)

for i in range(len(mt)):
    print(mt[i] - mt[i - 1])

plt.show()