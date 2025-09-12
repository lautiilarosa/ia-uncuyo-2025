
def h(tablero):
    h = 0
    for i in range(len(tablero)-1):
        for j in range(i+1,len(tablero)):
            # Estan en la misma fila?
            if tablero[i] == tablero[j]:
                h += 1
            else:
                #misma diagonal?
                if abs(tablero[i] - tablero[j]) == abs(i - j):
                    h += 1

    return h