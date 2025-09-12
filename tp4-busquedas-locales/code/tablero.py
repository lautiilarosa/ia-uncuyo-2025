import numpy as np
import random


def generar_tablero():
    n = int(input("Ingrese el tamaño del tablero: "))
    tablero = np.zeros(n, dtype=int)
    for i in range(n):
        tablero[i] = random.randint(0, n-1)  
    return tablero