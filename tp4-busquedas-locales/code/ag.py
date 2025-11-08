import numpy as np
from heuristic import h

class GeneticNQueens:
    def __init__(self, n, population_size, mutation_rate, max_generations, max_states):
        self.n = n
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.max_states = max_states

    # Fitness basado en h(tablero)
    def fitness(self, individual):
        return 1 / (1 + h(individual))

    # Crear un individuo aleatorio
    def random_individual(self):
        return np.random.randint(0, self.n, size=self.n)

    # Selección por torneo (k=3)
    def selection(self, population):
        k = 3
        indices = np.random.choice(len(population), k, replace=False)
        tournament = [population[i] for i in indices]
        fitness_values = np.array([self.fitness(ind) for ind in tournament])
        return tournament[np.argmax(fitness_values)]    

    
    def crossover(self, parent1, parent2):
        point = np.random.randint(1, self.n - 1)
        return np.concatenate((parent1[:point], parent2[point:]))

    
    def mutate(self, individual):
        if np.random.rand() < self.mutation_rate:
            idx = np.random.randint(0, self.n)
            individual[idx] = np.random.randint(0, self.n)

    
    def evolve(self, population):
        new_population = []
        fitness_values = np.array([self.fitness(ind) for ind in population])
        elite = population[np.argmax(fitness_values)].copy()
        new_population.append(elite)  # elitismo

        while len(new_population) < self.population_size:
            parent1 = self.selection(population)
            parent2 = self.selection(population)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)

        return new_population

   
    def run(self, initial_population):
        population = initial_population
        generations = 0

        for _ in range(self.max_generations):
            population = self.evolve(population)
            generations += 1

            fitness_values = np.array([self.fitness(ind) for ind in population])
            best_idx = np.argmax(fitness_values)
            best = population[best_idx]
            best_h = h(best)

            if best_h == 0:
                return best, best_h, generations  # devuelve la mejor solución encontrada

            if generations >= self.max_states:
                return best, best_h, generations  # devuelve lo mejor logrado aunque no sea solución

        return best, best_h, generations
