import csv
import utils.constants as cst
from modelisation.mcp import MaximumCoveringProblem
from algorithms.genetic import GeneticAlgorithm

# Nom du fichier CSV
csv_filename = f"results/experimentations/benchmark_global.csv"

# Hyperparamètres de l'algorithme génétique
ga_population_sizes = [20, 50, 100]
ga_crossover_rates =  [0.5, 0.8, 0.9]
ga_mutation_rates =   [0.01, 0.05, 0.1]
ga_generations =      [50, 100]
ga_points_croisements = [1, 3, 5]

for i, instance in enumerate(cst.BENCHMARKS):

    benchmark_name = instance[0] # nom du benchmark
    subsets, m, n, k = instance[1] # données du benchmark

    # Création d'une instance du problème MCP
    problem = MaximumCoveringProblem(subsets, k)

    # Ouvrir le fichier CSV en mode écriture
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Écrire l'en-tête du fichier CSV
        writer.writerow(["Algorithm", "Bench_id", "Pop_Size", "Crossover_Rate", "Mutation_Rate", "Generations", 
                        "Points_Croisement", "Fitness", "Execution_Time(s)"])

        # Exécution de la Grid Search pour GA
        for pop_size in ga_population_sizes:
            for crossover_rate in ga_crossover_rates:
                for mutation_rate in ga_mutation_rates:
                    for generations in ga_generations:
                        for points_croisement in ga_points_croisements:
                            
                            #GA
                            ga_solver = GeneticAlgorithm(problem, pop_size=pop_size, crossover_rate=crossover_rate,
                                                        mutation_rate=mutation_rate, generations=generations,
                                                        points_croisement=points_croisement)
                            solution, fitness, ga_time = ga_solver.run()
                            # Stocker le résultat dans le CSV
                            writer.writerow(["GA", benchmark_name, pop_size, crossover_rate, mutation_rate, generations,
                                            points_croisement, fitness, ga_time])

    print(f"\nBenchmark {i+1} ✅")
