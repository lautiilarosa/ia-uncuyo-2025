import csv
import random
import numpy as np
import time
from randomA import random_algorithm
from hillclimbing import hill_climbing
from simulated_annealing import simulated_annealing
from ag import GeneticNQueens
from heuristic import h

def main_experiment():
    sizes = [4, 8, 10]
    num_runs = 30
    max_states = 10000
    output_file = "resultados_n_reinas.csv"

    def run_random(tablero, max_states):
        solved, heur, estados = random_algorithm(tablero.copy(), max_states)
        return tablero, heur, estados

    def run_hill(tablero, max_states):
        solved, heur, estados = hill_climbing(tablero.copy(), max_states)
        return tablero, heur, estados

    def run_sim_annea(tablero, max_states):
        solved, heur, estados = simulated_annealing(tablero.copy(), max_states)
        return tablero, heur, estados

    def run_genetic(size, max_states):
        pop_size = 50
        mutation_rate = 0.1
        max_generations = max_states

        ga = GeneticNQueens(
            n=size,
            population_size=pop_size,
            mutation_rate=mutation_rate,
            max_generations=max_generations,
            max_states=max_states,
        )
        initial_population = [ga.random_individual() for _ in range(pop_size)]
        best, best_H, generations = ga.run(initial_population)
        return best.tolist(), best_H, generations


    algorithms = {
        "Random": run_random,
        "Hill Climbing": run_hill,
        "Simulated Annealing": run_sim_annea,
        "Genetic Algorithm": run_genetic,
    }

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["algorithm_name", "env_n", "size", "best_solution", "H", "states", "time"])

        env_id = 0
        for size in sizes:
            for seed in range(num_runs):
                random.seed(seed)
                np.random.seed(seed)
                env_id += 1

                tablero_inicial = [random.randint(0, size - 1) for _ in range(size)]

                for name, func in algorithms.items():
                    start = time.time()
                    if name == "Genetic Algorithm":
                        best_solution, best_H, states = func(size, max_states)
                    else:
                        best_solution, best_H, states = func(tablero_inicial.copy(), max_states)
                    elapsed = round(time.time() - start, 4)

                    writer.writerow([name, env_id, size, best_solution, best_H, states, elapsed])

    print(f"\n✅ Resultados guardados en {output_file}")

if __name__ == "__main__":
    main_experiment()
