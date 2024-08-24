import numpy as np
import random

class MaterialOptimizerGA:
    def __init__(self, material_lib, population_size=50, generations=100, mutation_rate=0.01):
        self.material_lib = material_lib
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.material_keys = ["density", "resistance", "thermal_expansion", "wear", "fatigue_limit"]  # Extend as needed

    def initialize_population(self):
        population = []

        # Choose each individual from the material library
        for _ in range(self.population_size):
            individual = random.choice(list(self.material_lib.values()))
            population.append(individual)

        return population
    
    def fitness_function(self, individual, target_properties, weight_factors):
        fitness = 0
        for key in self.material_keys:
            value = individual[key]
            if key == "density" and not (500 <= value <= 8000):
                fitness -= 1000  # Heavy penalty for unrealistic density
            elif key == "resistance" and not (50e9 <= value <= 300e9):
                fitness -= 1000  # Heavy penalty for unrealistic resistance
            elif key == "thermal_expansion" and not (5e-6 <= value <= 2.5e-5):
                fitness -= 1000  # Heavy penalty for unrealistic thermal expansion
            elif key == "wear" and not (1e-9 <= value <= 1e-7):
                fitness -= 1000  # Heavy penalty for unrealistic wear rate
            elif key == "fatigue_limit" and not (50e6 <= value <= 1e9):
                fitness -= 1000  # Heavy penalty for unrealistic fatigue limit
            else:
                fitness -= weight_factors[key] * np.abs(target_properties[key] - value)
        return fitness


    def select_parents(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [f / total_fitness for f in fitness_scores]
        parents = np.random.choice(population, size=2, p=probabilities)
        return parents

    def crossover(self, parent1, parent2):
        child = {}
        for key in self.material_keys:
            child[key] = parent1[key] if random.random() > 0.5 else parent2[key]
        return child
    

    def get_max_value(self, key):
        limits = {
            "density": 8000,
            "resistance": 300e9,
            "thermal_expansion": 2.5e-5,
            "wear": 1e-7,
            "fatigue_limit": 1e9
        }
        return limits[key]

    def get_min_value(self, key):
        limits = {
            "density": 500,
            "resistance": 50e9,
            "thermal_expansion": 5e-6,
            "wear": 1e-9,
            "fatigue_limit": 50e6
        }
        return limits[key]

    def mutate(self, individual):
        for key in self.material_keys:
            if random.random() < self.mutation_rate:
                mutation_value = random.uniform(-0.05, 0.05) * individual[key]  # Smaller mutation range
                individual[key] = max(min(individual[key] + mutation_value, self.get_max_value(key)), self.get_min_value(key))  # Ensure value stays within bounds

    def optimize_material(self, target_properties, weight_factors):
        population = self.initialize_population()
        
        for generation in range(self.generations):
            fitness_scores = [self.fitness_function(ind, target_properties, weight_factors) for ind in population]

            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                
                self.mutate(child1)
                self.mutate(child2)
                
                new_population.append(child1)
                new_population.append(child2)

            population = new_population
        
        final_fitness_scores = [self.fitness_function(ind, target_properties, weight_factors) for ind in population]
        best_individual = population[np.argmax(final_fitness_scores)]
        
        return best_individual

