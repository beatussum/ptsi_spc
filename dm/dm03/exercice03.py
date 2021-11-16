#! /usr/bin/env python3


from math import exp
import numpy

"""
Donneés de l'énoncé

On crée un `structured array` dont les champs (flottants) sont (dans l'ordre) :
 - `temperature` soit les valeurs de température spécifiées dans l'énoncé
 - `rate constant` soit les valeurs de la constante de vitesse également
    spécifiées dans l'énoncé
"""

data = numpy.array(
    [
        (0, 5.60e-5),
        (6, 11.80e-5),
        (12, 24.5e-5),
        (18, 48.8e-5),
        (24, 100e-5),
        (30, 208e-5)
    ],
    [("temperature", "f"), ("rate constant", "f")]
)

r = 8.314

"""
Conversion et traitement :
 - des degrés celcius en kelvins
 - on prend l'inverse de la température
 - on prend le logarithme de la constante de vitesse
"""

data["temperature"] += 273.15
data["temperature"] = 1 / data["temperature"]
data["rate constant"] = numpy.log(data["rate constant"])

"""
Régression linéaire et récupération des données
"""

a, b = numpy.polyfit(data["temperature"], data["rate constant"], 1)
act_energy = - r * a * 1e-3
exp_factor = exp(b)

"""
Affichage des résultats en écriture scientifique
"""

print(f"L'énergie d'activation de cette réaction est de {act_energy:.2e} kJ/mol.")
print(f"Le facteur de fréquence de cette réaction est de {exp_factor:.2e} L/mol s.")
