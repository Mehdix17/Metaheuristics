import random
import math
import time

#--------------------------------------- Fonctions -----------------------------------------

# génère une clique aléatoire pour l'opération 1
def random_clique(graph):

    # Selectionner un sommet aléatoire
    initial_vertex = random.choice(list(graph.keys()))

    # Ajouter tous les voisins du sommet initial qui forment une clique
    clique = set([initial_vertex])

    # Trier les voisins par degré dans l'ordre décroissant
    neighbors_with_degree = [(neighbor, len(graph[neighbor])) for neighbor in graph[initial_vertex]]
    neighbors_with_degree.sort(key=lambda x: x[1], reverse=True)

    # Ajout des voisins à la clique
    for neighbor, _ in neighbors_with_degree:
        if all(neigh in graph[neighbor] for neigh in clique):
            clique.add(neighbor)

    return clique if fitness(clique) > 1 else set()

# génère une clique aléatoire pour l'opération 2
def all_clique_random_clique(graph):

    # Selectionner un sommet aléatoire
    initial_vertex = random.choice(list(graph.keys()))

    # Ajouter tous les voisins du sommet initial qui forment une clique
    clique = set([initial_vertex])

    # Ajout des voisins à la clique
    for neighbor in graph[initial_vertex]:
        if all(neigh in graph[neighbor] for neigh in clique):
            clique.add(neighbor)

    return tuple(sorted(clique)) if fitness(clique) > 1 else set()

# génère une clique aléatoire pour l'opération 3
def random_vertex_clique(graph, vertex):

    # Ajouter tous les voisins du sommet initial qui forment une clique
    clique = set()
    clique.add(vertex)

    # Trier les voisins par degré dans l'ordre décroissant
    neighbors_with_degree = [(neighbor, len(graph[neighbor])) for neighbor in graph[vertex]]
    neighbors_with_degree.sort(key=lambda x: x[1], reverse=True)

    # Ajout des voisins à la clique
    for neighbor, _ in neighbors_with_degree:
        if all(neigh in graph[neighbor] for neigh in clique):
            clique.add(neighbor)
    
    return clique

# perturbe la soltuion actuelle pour obtenir une nouvelle solution
def perturb(graph, current_solution):

    if len(current_solution) <= 2:
        return random_clique(graph)
    
    probability = random.choice([0,1,1]) # 33 / 67

    perturbed_solution = set()
    if probability == 0: # Supprimer 2 sommets et les remplacer par un autre

        vertex1, vertex2 = random.sample(list(current_solution), 2)
        perturbed_solution = current_solution - {vertex1, vertex2}

        # Ajouter un nouveau sommet non inclus dans la clique qui forme toujours une clique
        for vertex in graph:
            if vertex not in perturbed_solution and all(neigh in perturbed_solution for neigh in graph[vertex]):
                perturbed_solution.add(vertex)
                break
    
    else:  # ajouter un sommet
        for vertex in graph:
            if vertex not in current_solution and all(neigh in current_solution for neigh in graph[vertex]):
                perturbed_solution.add(vertex)
                break

    return perturbed_solution if fitness(perturbed_solution) > 1 else set()

# perturbe la soltuion actuelle pour l'opération 3
def perturb_vertex_clique(graph, current_solution, vertex):

    if len(current_solution) <= 2:
        return random_vertex_clique(graph, vertex)
    
    probability = random.choice([0,1,1]) # 33 / 66

    if probability == 0: # Supprimer 2 sommets et les remplacer par un autre

        vertex1, vertex2 = random.sample(list(current_solution - {vertex}), 2)
        perturbed_solution = current_solution - {vertex1, vertex2}

        # Ajouter un nouveau sommet non inclus dans la clique qui forme toujours une clique
        for vertex_to_add in graph:
            if vertex_to_add not in perturbed_solution and all(neigh in perturbed_solution for neigh in graph[vertex_to_add]):
                perturbed_solution.add(vertex_to_add)
                break
    
    else:  # ajouter un sommet
        perturbed_solution = current_solution.copy()
        for vertex_to_add in graph:
            if check_vertex(perturbed_solution, vertex_to_add, graph):
                perturbed_solution.add(vertex_to_add)
                break

    return perturbed_solution

# Function to check if a vertex addition maintains the clique property
def check_vertex(clique, vertex_to_add, graph):
    return (vertex_to_add not in clique) and all(vertex_to_add in graph[neigh] for neigh in clique)

# Fonction objectif
def fitness(solution):
    return len(solution)

#--------------------------------------- Opération 1 -----------------------------------------

def maximum_clique_finder(graph, initial_temperature, cooling_rate, nb_iterations, timer):

    # Initialisation
    current_solution = random_clique(graph)
    best_solution = current_solution
    temperature = initial_temperature

    start_time = time.time()

    for _ in range(nb_iterations):

        # Générer une solution voisine
        neighbor_solution = perturb(graph, current_solution)

        # Calculer la fitness de la solution
        current_score = fitness(current_solution)
        neighbor_score = fitness(neighbor_solution)

        # Calcul de la probabilité d'acceptation de Boltzmann
        probability = math.exp((neighbor_score - current_score) / temperature)

        # Acceptation de la solution voisine
        if neighbor_score >= current_score or random.random() < probability :
            current_solution = neighbor_solution

        # Mise à jour de la meilleure solution
        if fitness(current_solution) > fitness(best_solution):
            best_solution = current_solution

        # Diminution progressive de la température
        temperature = initial_temperature * (1 / (1 + cooling_rate * math.log(nb_iterations + 1)))

        if timer and (time.time() - start_time > timer):
            break

    end_time = time.time()
    
    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)
    
    return sorted(best_solution), calcul_time

#--------------------------------------- Opération 2 -----------------------------------------

def all_clique_finder(graph, initial_temperature, cooling_rate, nb_iterations, timer):

    # Initialize with an empty set to store all cliques
    all_cliques = set()
    current_solution = random_clique(graph)
    temperature = initial_temperature
    start_time = time.time()

    for _ in range(nb_iterations):

        neighbor_solution = perturb(graph, current_solution)

        # Calculer la fitness de la solution
        current_score = fitness(current_solution)
        neighbor_score = fitness(neighbor_solution)

        # Calcul de la probabilité d'acceptation de Boltzmann
        probability = math.exp((neighbor_score - current_score) / temperature)

        # Acceptation de la solution voisine
        if neighbor_score >= current_score or random.random() < probability :
            current_solution = neighbor_solution
            new_clique = tuple(sorted(neighbor_solution))
            if new_clique not in all_cliques:
                all_cliques.add(new_clique)
                
        if timer and (time.time() - start_time > timer):
            break
        
        # Diminution progressive de la température
        temperature = initial_temperature * (1 / (1 + cooling_rate * math.log(nb_iterations + 1)))
    
    end_time = time.time()
    
    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)
    
    all_cliques.discard(())
    return sorted(all_cliques, key=len), calcul_time

#--------------------------------------- Opération 3 -----------------------------------------

def vertex_maximum_clique_finder(graph, vertex, initial_temperature, cooling_rate, nb_iterations, timer):

    # Initialize with a clique containing only the given vertex
    current_solution = set()
    current_solution.add(vertex)
    best_solution = current_solution
    temperature = initial_temperature
    initial_vertex = vertex

    start_time = time.time()

    for _ in range(nb_iterations):

        # Find valid neighbors to potentially add to the current solution
        valid_neighbors = [neigh for neigh in graph[vertex] if check_vertex(current_solution, neigh, graph)]
        
        # Select a random valid neighbor
        if valid_neighbors:
            neighbor_to_add = random.choice(valid_neighbors)
            current_solution.add(neighbor_to_add)
            vertex = neighbor_to_add  # Update vertex for next iteration (focus on recently added neighbor)

        else:
            # Update best solution if it's a larger clique containing the vertex
            if fitness(current_solution) > fitness(best_solution):
                best_solution = current_solution.copy()

            # perturber la solution actuelle pour sortir de l'optimum local
            neighbor_solution = perturb_vertex_clique(graph, current_solution, initial_vertex)

            # Calculate fitness (size) of both solutions
            current_score = fitness(current_solution)
            neighbor_score = fitness(neighbor_solution)

            # Probability of accepting the neighbor solution based on Boltzmann distribution
            probability = math.exp((neighbor_score - current_score) / temperature)

            # Accept the neighbor solution if it improves fitness or randomly with a certain probability
            if neighbor_score >= current_score or random.random() < probability:
                current_solution = neighbor_solution

        # Gradually decrease temperature
        temperature = initial_temperature * (1 / (1 + cooling_rate * math.log(nb_iterations + 1)))

        if timer and (time.time() - start_time > timer):
            break
    
    end_time = time.time()
    
    # Calculer le temps d'exécution
    calcul_time = round(end_time - start_time, 2)

    return sorted(best_solution), calcul_time
