#! /usr/bin/env python3


import matplotlib.pyplot as plt

## Données

R    = 8.314 # en u.s.i.

Pmin = 800   # en hectopascal
Tmin = 290   # en kelvin
Tmax = 450   # en kelvin
Vmax = 44    # en centimètre cube
Vmin = 32    # en centimètre cube

n = (Pmin * Vmin) / (R * Tmin)

def Cycle(
    n: float,
    Vmin: float,
    Tmin: float,
    Tmax: float,
    N: int
) -> tuple[list[float], list[float], list[float]]:

    Pbas   = []
    Phaut  = []
    listeV = []

    for k in range(N):
        V = Vmin + k * ((Vmax - Vmin) / N)

        Pbas.append((n * R * Tmin) / V)
        Phaut.append((n * R * Tmax) / V)
        listeV.append(V)

    return (listeV, Pbas, Phaut)

def rectangle(N: int) -> float:
    _, pbas, phaut = Cycle(n, Vmin, Tmin, Tmax, N)

    ret = 0

    for (a, b) in zip(pbas, phaut):
        ret += a - b

    ret *= (Vmax - Vmin) / N

    return ret

## Question 5

print("""

==== Question 5 ====

""")

plt.figure("Cycle de Stirling")

listev, pbas, phaut = Cycle(n, Vmin, Tmin, Tmax, 500)

x = listev + listev[::-1] + [listev[0]]
y = pbas + phaut + [pbas[0]]

plt.plot(x, y, "r", label = "$ P(V) $")

plt.title("Cycle de Stirling")
plt.xlabel("Volume (en centimètre cube)")
plt.ylabel("Pression (en hectopascal)")
plt.legend()
plt.grid()

plt.show()

## Question 6

print(f"""

==== Question 6 ====

On trouve un travail de `{rectangle(500):.2e}` joule.

""")
