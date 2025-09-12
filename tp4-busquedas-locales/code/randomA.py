import random
from heuristic import h

def random_algorithm(tablero,max_estados):
    if h(tablero) == 0:
        return True,1
    
    estados = 1
    while estados < max_estados:
        column = random.randint(0,len(tablero)-1)
        fila = random.randint(0,len(tablero)-1)
        while fila == column:
            fila = random.randint(0,len(tablero)-1)

        tablero[column] = fila
        estados += 1
        if h(tablero) == 0:
            return True,estados
        
    return False,h(tablero)
    