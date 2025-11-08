import random
from heuristic import h

def random_algorithm(tablero, max_estados):
    if h(tablero) == 0:
        return True, 0, 1
    
    estados = 1
    while estados < max_estados:
        column = random.randint(0, len(tablero) - 1)
        fila = random.randint(0, len(tablero) - 1)

        # Evitar mover a la misma fila
        while fila == tablero[column]:
            fila = random.randint(0, len(tablero) - 1)

        tablero[column] = fila
        estados += 1

        heuristica = h(tablero)
        if heuristica == 0:
            return True, 0, estados

    return False, h(tablero), estados
