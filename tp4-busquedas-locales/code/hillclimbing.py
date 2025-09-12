from heuristic import h
       
def col_conflictiva(tablero):
    max_conflictos = -1
    worst_col = 0
     
    for col in range(len(tablero)):
        # Calcular conflictos para esta columna específica
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


def move_queen(tablero,col):
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


def hill_climbing(tablero,max_estados):
    """
    1) Calculamos primero la heuristica de la tabla y si es igual a 0 retornamos resultados
    2) Caso contrario iremos buscando la reina o columna que tenga mas pares amenazados
    3) Moveremos la reina a una celda en donde tenga la menor cantidad de pares amenazados
    4) repetimos hasta que la heuristica de 0
    """
    #Primera variable es si h(t) = 0 , la segunda la cantidad de estados alcanzados
    if h(tablero) == 0:
        return True,1
    
    estados = 1
    while estados < max_estados:
        col = col_conflictiva(tablero)
        move_queen(tablero,col)

        if h(tablero) == 0:
            return True,estados
         
        estados += 1

    return False,h(tablero)
