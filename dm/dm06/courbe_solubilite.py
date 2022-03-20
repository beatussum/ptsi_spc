#! /usr/bin/env python3


from math import log10
import matplotlib.pyplot as plt
import numpy

pke = 14          # sans unité
ke  = 10**(- pke) # sans unité

c       = 1e-3 # en mole par litre
cp      = 1e-4 # en mole par litre
cpp     = 1e-9 # en mole par litre
ph_test = 10

ph_a = 7.3  # sans unité
ph_b = 13.0 # sans unité

pks = - log10(c) + 2 * pke - 2 * ph_a # sans unité
ks  = 10**(- pks)                     # sans unité

pk = - log10(c) - 2 * pke + 2 * ph_b # sans unité
k  = 10**(- pk)                      # sans unité

pbeta = pk - pks # sans unité

ph_asymp_a = ( ( pbeta - 2 ) / 4 ) + pke # sans unité
ph_asymp_b = ( ( pbeta + 2 ) / 4 ) + pke # sans unité

def s(ph: float) -> float:
    return ( ks / ke**2 ) * 10**(- 2 * ph) + ( ke**2 * k ) * 10**(2 * ph)

def s_asymp_a(ph: float) -> float:
    return - 2 * ph - pks + 2 * pke

def s_asymp_b(ph: float) -> float:
    return 2 * ph - 2 * pke - pk

def show() -> None:
    ph_list = numpy.linspace(ph_a, ph_b)

    ph_list_asymp_a = numpy.linspace(ph_a, ph_asymp_a + 1)
    ph_list_asymp_b = numpy.linspace(ph_asymp_b - 1, ph_b)

    plt.figure("Évolution de la solubilité en fonction du pH.")
    plt.title("Évolution de la solubilité en fonction du pH.")
    plt.xlabel(r"$ pH $")
    plt.ylabel("solubilité (en échelle logarithmique)")
    plt.grid()
    plt.legend()

    plt.hlines(log10(c), 0, ph_a, color = "k", linestyle = "--")
    plt.hlines(log10(c), ph_b, 14, color = "k", linestyle = "--")

    plt.plot(
        ph_list, numpy.log10(numpy.vectorize(s)(ph_list)),
        "r",
        label = r"$ \log(s) $"
    )

    # Question 8
    plt.hlines(log10(cp), 0, 10, color = "b", linestyle = "--")
    plt.hlines(log10(cpp), 0, 12, color = "b", linestyle = "--")
    plt.vlines(ph_test, -9, -6, color = "b", linestyle = "--")

    # Asymptotes
    plt.plot(ph_list_asymp_a, numpy.vectorize(s_asymp_a)(ph_list_asymp_a), "--k")
    plt.plot(ph_list_asymp_b, numpy.vectorize(s_asymp_b)(ph_list_asymp_b), "--k")

    plt.show()

show()
