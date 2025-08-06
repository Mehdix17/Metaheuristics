import csv
import itertools
import threading
import utils.constants as cst
from concurrent.futures import ThreadPoolExecutor
from modelisation.mcp import MaximumCoveringProblem
from algorithms.genetic import GeneticAlgorithm

def generate_param_combinations(param_grid):
    return list(itertools.product(*param_grid.values()))

def run_ga(problem, params):
    pop_size, crossover_rate, mutation_rate, generations, points_croisement = params
    
    ga_solver = GeneticAlgorithm(problem, pop_size=pop_size, crossover_rate=crossover_rate,
                                 mutation_rate=mutation_rate, generations=generations,
                                 points_croisement=points_croisement)
    _, fitness, ga_time = ga_solver.run()
    return list(params) + [fitness, ga_time]

def save_results(csv_filename, results, lock):
    with lock:
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(results)

def run_grid_search(param_combinations, problem, csv_filename, num_threads, benchmark_id):
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(lambda params: run_ga(problem, params), param_combinations))
    # Prepend benchmark_id to each result row
    results = [[benchmark_id] + res for res in results]
    save_results(csv_filename, results, lock)

def main():
    csv_filename = f"results/experimentations/benchmark_global.csv"
    param_grid = {
        "population_size": [20, 50, 100],
        "crossover_rate": [0.5, 0.8, 0.9],
        "mutation_rate": [0.01, 0.05, 0.1],
        "Generations": [20, 60],
        "points_croisement": [1, 3, 5]
    }
    param_combinations = generate_param_combinations(param_grid)
    num_threads = 4
    
    # with open(csv_filename, mode="w", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Bench_id","Pop_Size", "Crossover_Rate", "Mutation_Rate", "Generations", "Points_Croisement", "Fitness", "Execution_Time(s)"])
    
    for i, benchmark in enumerate(cst.BENCHMARKS, start=1):
        print(f"Exécution du benchmark {i} ({benchmark[0]})...")
        # subsets = benchmark[1][0], k = benchmark[1][3]
        problem = MaximumCoveringProblem(benchmark[1][0], benchmark[1][1], benchmark[1][3])  
        run_grid_search(param_combinations, problem, csv_filename, num_threads, benchmark[0])
        print(f"Benchmark {i} ✅")

if __name__ == "__main__":
    main()
