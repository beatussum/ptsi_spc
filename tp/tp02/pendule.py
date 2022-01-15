#! /usr/bin/env python3


from math import log
import matplotlib.pyplot as plt
import numpy

def read_file(file_name):
    content = numpy.loadtxt(file_name)

    return (content[:, 0], content[:, 1])

def find_maxima(times, theta):
    maximum       = True
    maximum_index = []
    maximum_times = []
    maximum_theta = []

    for i in range(1, len(times)):
        if theta[i] < 0:
            continue

        if times[i] > 20:
            break

        if ( theta[i - 1] < theta[i] ) == maximum:
            maximum = not maximum

            if maximum:
                maximum_index.append(i)
                maximum_times.append(times[i])
                maximum_theta.append(theta[i])

    return (maximum_index, maximum_times, maximum_theta)

def compute_period(times, theta):
    _, maxima_times, _ = find_maxima(times, theta)

    return ( maxima_times[-1] - maxima_times[0] ) / ( len(maxima_times) - 1 )

def logarithmic_decrement(times, theta, period):
    first_period, *_, last_period = find_maxima(times, theta)[0]

    delta     = []
    theta_inf = theta[-1]

    def theta_at(t):
        for i in range(1, len(times)):
            if times[i] == t:
                return theta[i]
            elif times[i] > t:
                a = ( theta[i] - theta[i - 1] ) / ( times[i] - times[i - 1] )

                return a * ( t - times[i - 1] ) + theta[i - 1]

        return theta_inf

    for i in range(first_period, last_period + 1):
        d = ( theta[i] - theta_inf ) / ( theta_at(theta[i] + period) - theta_inf )
        delta.append(d)

    return log(numpy.average(d))

""" def logarithmic_decrement(times, theta, _):
    _, maximum_times, maximum_theta = find_maxima(times, theta)

    delta     = []
    theta_inf = theta[-1]

    for i in range(1, len(maximum_times)):
        d = ( maximum_theta[i - 1] - theta_inf ) / ( maximum_theta[i] - theta_inf )
        delta.append(d)

    return log(numpy.average(d)) """

"""
Étalonnage
"""

h         = 28                                                  # en centimètre
positions = numpy.array([0, 1.5, 3, 4.5, 6, 7.5, 9])            # en centimètre
tensions  = numpy.array([5.70, 5.0, 4.4, 3.5, 2.70, 1.9, 1.35]) # en centimètre

theta = numpy.arctan2(positions, h)

a, b = numpy.polyfit(tensions, theta, 1)

plt.figure(0)
plt.title("Étalonnage du capteur angulaire")
plt.plot(tensions, theta, "r+", label = "expérimental")
plt.plot(tensions, a * tensions + b, "b", label = "régression linéaire")
plt.xlabel("tension (en volt)")
plt.ylabel("angle (en radian)")
plt.grid()
plt.legend()

"""
Traitement des données
"""

exp_times, exp_tensions = read_file("pendule.txt")

exp_theta = a * exp_tensions + b

plt.figure(1)
plt.title(r"Évolution temporelle de $ \theta $")
plt.plot(exp_times, exp_theta, "b")
plt.xlabel("temps (en seconde)")
plt.ylabel(r"$ \theta $ (en radian)")
plt.grid()

period = compute_period(exp_times, exp_theta)
delta  = logarithmic_decrement(exp_times, exp_theta, period)

plt.show()