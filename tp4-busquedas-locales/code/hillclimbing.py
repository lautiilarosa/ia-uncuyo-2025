from heuristic import h
import numpy as np

def col_conflictiva(tablero):
    max_conflictos = -1
    worst_col = 0
    for col in range(len(tablero)):
        conflictos = 0
        for otra_col in range(len(tablero)):
            if otra_col == col:
                continue
            if tablero[col] == tablero[otra_col]:
                conflictos += 1
            elif abs(tablero[col] - tablero[otra_col]) == abs(col - otra_col):
                conflictos += 1

        if conflictos > max_conflictos:
            max_conflictos = conflictos
            worst_col = col
    return worst_col


def move_queen(tablero, col):
    row_elegida = tablero[col]
    min_h = float("inf")
    for i in range(len(tablero)):
        if i == tablero[col]:
            continue
        copy = tablero.copy()
        copy[col] = i
        new_h = h(copy)
        if new_h < min_h:
            min_h = new_h
            row_elegida = i
    tablero[col] = row_elegida


def hill_climbing(tablero, max_estados):
    """
    Retorna:
    - solved (bool): si encontró solución
    - heuristica_final (int)
    - estados_usados (int)
    """
    if h(tablero) == 0:
        return True, 0, 1

    estados = 1
    while estados < max_estados:
        col = col_conflictiva(tablero)
        move_queen(tablero, col)
        estados += 1
        heur = h(tablero)
        if heur == 0:
            return True, heur, estados

        if estados % 100 == 0:
            tablero = np.random.randint(0, len(tablero), size=len(tablero))

    # No encontró solución dentro del límite
    return False, h(tablero), estados
