import random
import time

class GeneticAlgorithm:
    def __init__(self, problem, pop_size=20, crossover_rate=0.5, mutation_rate=0.1, generations=20, points_croisement=3):
        self.problem = problem
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.points_croisement = points_croisement
        self.num_subsets = len(problem.subsets)

        # Générer la population initiale # (0, 1, 2, 55, k-1) k elements
        self.population = [random.sample(range(self.num_subsets), self.problem.k) for _ in range(pop_size)]
        # population = [ 
            # [ S1, S2, S3, ...  ] # individu 1
            # [ S2, S5, S8, ...  ] # individu 2
            # [ S9, S12, S30, ...] # individu pop_size (20)
        # ]

    def evaluate(self, solution):
        selected_subsets = [self.problem.subsets[i] for i in solution]
        covered_elements = set().union(*selected_subsets)
        return len(covered_elements)

    def select_parent(self):
        return max(random.sample(self.population, 3), key=self.evaluate)

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate: # 0.5 < 0.8 --> faire le crossover 
                                                  # 0.9 > 0.8 --> retourner les parents 

            # Générer n points de croisement uniques
            points = sorted(random.sample(range(1, self.problem.k), self.points_croisement))
            
            # Initialiser les enfants
            child1 = parent1.copy()
            child2 = parent2.copy()
            
            # Alterner les segments entre les points de croisement
            switch = False
            start = 0
            
            for point in points: # points = [10, 70, 98]
                
                if switch:
                    child1[start:point] = parent1[start:point] # parent1[0 : 10] -> parent2[10 : 70] -> parent2[70 : 98]
                    child2[start:point] = parent2[start:point] # parent2[0 : 10] -> parent2[10 : 70] -> parent2[70 : 98]
                else:
                    child1[start:point] = parent2[start:point] # parent2[0 : 10] -> parent2[10 : 70] -> parent2[70 : 98]
                    child2[start:point] = parent1[start:point] # parent1[0 : 10] -> parent2[10 : 70] -> parent2[70 : 98]
                
                switch = not switch
                start = point
            
            # Gérer le dernier segment
            if switch:
                child1[start:] = parent1[start:] # parent2[98 : k]
                child2[start:] = parent2[start:] # parent2[98 : k]
            else:
                child1[start:] = parent2[start:] # parent2[98 : k]
                child2[start:] = parent1[start:] # parent2[98 : k]
                
            return child1, child2
        
        return parent1.copy(), parent2.copy()

    def mutate(self, solution):
        if random.random() < self.mutation_rate:
            index = random.randint(0, self.problem.k - 1)
            new_subset = random.choice(range(self.num_subsets)) 
            solution[index] = new_subset
        return solution
        
        # solution = [0, 4, 9, 5, 8]
        # index = 3
        # new_subset = 17
        # solution[index] = new_subset donc solution[3] = 17
        # solution = [0, 4, 9, 17, 8]
    
    def run(self):
        best_solution = []
        best_fitness = 0
        start_time = time.time()

        for i in range(self.generations):
            new_population = []
            
            for _ in range(self.pop_size // 2):
                parent1, parent2 = self.select_parent(), self.select_parent()
                child1, child2 = self.crossover(parent1, parent2)
                child1, child2 = self.mutate(child1), self.mutate(child2)
                new_population.extend([child1, child2])

            self.population = new_population

            current_best = max(self.population, key=self.evaluate)
            current_fitness = self.evaluate(current_best)

            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_solution = current_best.copy()
                print(f"\nGeneration {i+1} : {current_fitness}")
            
        exec_time = time.time() - start_time

        return best_solution, best_fitness, round(exec_time, 2)
