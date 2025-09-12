import numpy as np
import random
from tablero import generar_tablero
from hillclimbing import hill_climbing
from heuristic import h
from simulated_annealing import sim_annea
from randomA import random_algorithm


if __name__ == "__main__":
    tablero = generar_tablero()
    estados = int(input("Ingrese el número de estados: "))

    print(f"El tablero inicializado: {tablero}")
    print(f"El tablero con heuristica de : {h(tablero)}")

    #bool_,int_ = hill_climbing(tablero,estados)
    #bool_,int_ = sim_annea(tablero,estados)
    bool_,int_ = random_algorithm(tablero,estados)

    print("")

    print(f"El tablero resultante : {tablero}")

    if bool_ == True:
        print(f"Se alcanzó la solucion con : {int_} , estados en total")
    else:
        print(f"Se alcanzó la máxima cantidad de estados con un H de : {int_}")
