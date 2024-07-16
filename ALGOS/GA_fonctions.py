import random
import time

#--------------------------------------- Fonctions -----------------------------------------

# génère une clique aléatoire
def random_clique(graph, max_neighbors):
    
    initial_vertex = random.choice(list(graph.keys()))
    clique = set([initial_vertex])
    neighbors_with_degree = [(neighbor, len(graph[neighbor])) for neighbor in graph[initial_vertex]]
    neighbors_with_degree.sort(key=lambda x: x[1], reverse=True)
    
    if max_neighbors: # Limiter les voisins considérés
        neighbors_with_degree = neighbors_with_degree[:max_neighbors]
    
    for neighbor, _ in neighbors_with_degree:
        if all(neigh in graph[neighbor] for neigh in clique):
            clique.add(neighbor)

    return clique if fitness(clique) > 1 else set()

# génère une clique aléatoire pour l'opération 3
def random_vertex_clique(graph, vertex):
    clique = set([vertex])
    neighbors_with_degree = [(neighbor, len(graph[neighbor])) for neighbor in graph[vertex]]
    neighbors_with_degree.sort(key=lambda x: x[1], reverse=True)
    
    for neighbor, _ in neighbors_with_degree:
        if all(neigh in graph[neighbor] for neigh in clique):
            clique.add(neighbor)

    return clique

# Fonction de croisement entre deux parents
def crossover(graph, parent1, parent2, crossover_rate):
    
    if random.random() < crossover_rate:
        parent1_list = list(parent1)
        parent2_list = list(parent2)
        crossover_point = random.randint(0, min(len(parent1_list), len(parent2_list)))
        child_list = parent1_list[:crossover_point] + parent2_list[crossover_point:]
        child = set(child_list)
        if all(neigh in graph[vertex] for vertex in child for neigh in child if vertex != neigh):           
            return child
    
    return set(parent1) if random.random() < 0.5 else set(parent2)

# Fonction de mutation
def mutation(graph, solution, mutation_rate):
    
    if random.random() < mutation_rate:
        non_clique_vertices = [vertex for vertex in graph if vertex not in solution]
        if non_clique_vertices:
            vertex_to_add = random.choice(non_clique_vertices)
            if all(neigh in graph[vertex_to_add] for neigh in solution):
                solution.add(vertex_to_add)
    
    return solution

# Fonction de sélection basée sur la roue de roulette
def selection(population):
    weights = [fitness(sol) for sol in population]
    total_fitness = sum(weights)
    
    if total_fitness == 0:
        return random.choice(population), random.choice(population)
    
    weights = [w / total_fitness for w in weights]  
    return random.choices(population, weights=weights, k=2)

# Fonction objectif
def fitness(solution):
    return len(solution)

#--------------------------------------- Opération 1 -----------------------------------------

def maximum_clique_finder(graph, population_size, mutation_rate, crossover_rate, generations, timer):
    
    # Initialiser la population
    population = [random_clique(graph, None) for _ in range(population_size)]
    best_solution = max(population, key=fitness)

    start_time = time.time()

    # Simulation de générations
    for _ in range(generations):
        selected_parents = selection(population)
        child = crossover(graph, selected_parents[0], selected_parents[1], crossover_rate)
        child = mutation(graph, child, mutation_rate)

        # Remplacer la pire solution
        population.remove(min(population, key=fitness))
        population.append(child)

        # Mettre à jour la meilleure solution
        if fitness(child) > fitness(best_solution):
            best_solution = child

        # Vérifier la limite de temps d'exécution
        if timer and time.time() - start_time > timer:
            break

    end_time = time.time()

    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)

    # Cas où aucune clique n'a été trouvée
    if fitness(best_solution) < 1:
        best_solution = set()

    return sorted(best_solution), calcul_time

#--------------------------------------- Opération 2 -----------------------------------------

def all_clique_finder(graph, population_size, mutation_rate, crossover_rate, generations, timer):
  
    # Initialize an empty set to store all found cliques
    all_cliques = set()

    # Generate initial population
    population = [random_clique(graph, 5) for _ in range(population_size)]

    start_time = time.time()

    for _ in range(generations):
        selected_parents = random.choices(population, k=2)
        child = crossover(graph, selected_parents[0], selected_parents[1], crossover_rate)
        child = mutation(graph, child, mutation_rate)

        # Ajouter child à all_clique s'il n'y est pas et si sa taille est supérieur à 1 (sommet non isolé)
        new_clique = tuple(sorted(child))
        if new_clique not in all_cliques and fitness(new_clique) > 1:
            all_cliques.add(new_clique)
        
        # Agrandir la population
        population.append(child)

        # Vérifier la limite de temps d'exécution
        if timer and (time.time() - start_time > timer):
            break

    end_time = time.time()

    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)
    
    # Enlever le tuple vide créé lors de l'initialisation
    all_cliques.discard(())

    return sorted(list(all_cliques), key=len), calcul_time

#--------------------------------------- Opération 3 -----------------------------------------

def vertex_maximum_clique_finder(graph, vertex, population_size, mutation_rate, crossover_rate, generations, timer):
    
    population = [random_vertex_clique(graph, vertex) for _ in range(population_size)]
    best_solution = max(population, key=fitness)

    start_time = time.time()

    for _ in range(generations):
        selected_parents = selection(population)
        child = crossover(graph, selected_parents[0], selected_parents[1], crossover_rate)
        child = mutation(graph, child, mutation_rate)

        if fitness(child) > fitness(min(population, key=fitness)):
            population.remove(min(population, key=fitness))
            population.append(child)

        if fitness(child) > fitness(best_solution):
            best_solution = child

        # Vérifier la limite de temps d'exécution
        if timer and (time.time() - start_time > timer):
            break

    end_time = time.time()

    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)

    return sorted(best_solution), calcul_time


