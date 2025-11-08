import numpy as np
import random
from tablero import generar_tablero
from hillclimbing import hill_climbing
from heuristic import h
from simulated_annealing import simulated_annealing
from randomA import random_algorithm
from ag import GeneticNQueens
import csv
from experimento import main_experiment 



if __name__ == "__main__":
    """
    #tablero = generar_tablero()
    estados = int(input("Ingrese el número de estados: "))
    #print(f"El tablero inicializado: {tablero}")
    #print(f"El tablero con heuristica de :         {h(tablero)}")

    #bool_,int_ = hill_climbing(tablero,estados)
    #bool_,int_ = sim_annea(tablero,estados)
    #bool_,int_ = random_algorithm(tablero,estados)
    n = int(input("Ingrese el tamaño del tablero: "))
    ga = GeneticNQueens(n, population_size=100, mutation_rate=0.1, max_generations=1000, max_states=estados,solution = False)
    initial_population = [ga.random_individual() for _ in range(ga.population_size)]
    solution, total_states = ga.run(initial_population)

    print("Tablero final encontrado:", solution)
    print("Número de conflictos:", ga.h(solution))
    print("Cantidad de estados evaluados:", total_states)

    #print("")

    #print(f"El tablero resultante : {tablero}")

    #if bool_ == True:
        #print(f"Se alcanzó la solucion con : {int_} , estados en total")
    #else:
        #print(f"Se alcanzó la máxima cantidad de estados con un H de : {int_}")
    
    
    """
    main_experiment()


    