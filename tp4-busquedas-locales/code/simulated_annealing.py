from heuristic import h
import random
import math

def schedule(T):
    """
    Plantaeamos un schedule geométrico con a = 0.9
    """
    a = 0.9
    return a * T


def sim_annea(tablero,max_estados):
    if h(tablero) == 0:
        return True,1

    T = 100
    estados = 1

    while estados < max_estados and T > 1 :
        column = random.randint(0, len(tablero)-1)
        fila = random.randint(0, len(tablero)-1)
        while fila == tablero[column]:
            fila = random.randint(0, len(tablero)-1)
        
        copy = tablero.copy()
        copy[column] = fila
        delta = h(copy) - h(tablero)

        if delta < 0:
            tablero[column] = fila
        else:
            prob = math.exp(-delta / T)
            r = random.random()
            if r < prob:
                tablero[column] = fila
        

        T = schedule(T)
        estados += 1
        if h(tablero) == 0:
            return True,estados
    
    return False,h(tablero)