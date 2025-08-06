import csv
import utils.constants as cst
from modelisation.mcp import MaximumCoveringProblem
from algorithms.genetic import GeneticAlgorithm
from algorithms.dfs import DepthFirstSearch

filename = cst.EXPERIMENTATION_PATH + "comparaison.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Écrire l'en-tête du fichier CSV
    writer.writerow(["Algorithm", "Bench_id", "m", "n", "k", "Fitness", "Execution_Time(s)"])

    for i, instance in enumerate(cst.BENCHMARKS):

        benchmark_name = instance[0] # nom du benchmark
        subsets, m, n, k = instance[1] # données du benchmark

        # Création d'une instance du problème MCP
        problem = MaximumCoveringProblem(subsets, m, k)

        # GA
        ga_solver = GeneticAlgorithm(problem)

        solution, fitness, ga_time = ga_solver.run()
        writer.writerow(["GA", benchmark_name, m, n, k, fitness, ga_time])

        #DFS
        dfs_solver = DepthFirstSearch(problem, limit=10)

        solution, fitness, dfs_time = dfs_solver.run()
        writer.writerow(["DFS", benchmark_name, m, n, k, fitness, dfs_time])
        
        print(f"\nBenchmark {i+1} ✅")
