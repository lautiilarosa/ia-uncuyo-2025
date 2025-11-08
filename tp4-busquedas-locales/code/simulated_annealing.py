from heuristic import h
import random
import math

def schedule(T):
    """
    Schedule geométrico con factor de enfriamiento a = 0.9.
    """
    a = 0.9
    return a * T

def simulated_annealing(tablero, max_estados):
    """
    Algoritmo de Recocido Simulado (Simulated Annealing).
    Intenta minimizar la heurística H(tablero) mediante un proceso de
    exploración con probabilidad de aceptar peores movimientos al inicio.
    """
    H_actual = h(tablero)
    if H_actual == 0:
        return True, H_actual, 1  

    T = 100
    estados = 1

    while estados < max_estados and T > 1:
        column = random.randint(0, len(tablero) - 1)
        fila = random.randint(0, len(tablero) - 1)
        while fila == tablero[column]:
            fila = random.randint(0, len(tablero) - 1)

        copy = tablero.copy()
        copy[column] = fila
        delta = h(copy) - H_actual

        if delta < 0:
            tablero[column] = fila
            H_actual = h(tablero)
        else:
            prob = math.exp(-delta / T)
            if random.random() < prob:
                tablero[column] = fila
                H_actual = h(tablero)

        T = schedule(T)
        estados += 1

        if H_actual == 0:
            return True, 0, estados

    return False, H_actual, estados
