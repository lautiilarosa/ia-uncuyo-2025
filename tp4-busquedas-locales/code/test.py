import numpy as np
from ag import GeneticNQueens
from heuristic import h

# --- Configuración ---
n = 8
population_size = 100
mutation_rate = 0.1
max_generations = 200
max_states = 10000


ga = GeneticNQueens(n, population_size, mutation_rate, max_generations, max_states)


initial_population = [ga.random_individual() for _ in range(population_size)]


best, best_h, generations = ga.run(initial_population)


print(f"\n🔹 Mejor solución encontrada: {best}")
print(f"🔹 Valor de H(best): {best_h}")
print(f"🔹 Generaciones usadas: {generations}")


if h(best) == 0:
    print("Se encontró una solución válida (sin conflictos).")
else:
    print("No se encontró una solución perfecta.")
