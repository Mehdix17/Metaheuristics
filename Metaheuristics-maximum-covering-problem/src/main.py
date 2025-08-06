from utils import constants as cst
from modelisation.mcp import MaximumCoveringProblem
from utils.utils import display_menu, file_maker, execute_algorithm, display_solution, save_csv

while True:

    # afficher le menu et récupréer la réponse de l'utilisateur
    instance_list, algo_code = display_menu()

    # traitrer les cas où l'utilisateur a choisi au moins un benchmark
    if instance_list:

        file_path = file_maker()
        
        # Préparer les données des benchmarks sélectionnés
        benchmark_data = []

        for instance in instance_list:
            benchmark_name = instance[0] # nom du benchmark
            subsets, m, n, k = instance[1] # données du benchmark

            # Création d'une instance du problème MCP
            problem = MaximumCoveringProblem(subsets, m, k)

            # Définir les algorithmes à exécuter selon le choix de l'utilisateur
            algorithms = []
            if algo_code == 1:
                algorithms.append(cst.ALGOS[0])
            elif algo_code == 2:
                algorithms.append(cst.ALGOS[1])
            else:  # Exécuter les deux
                algorithms.extend(cst.ALGOS)

            # Exécuter et afficher les résultats pour chaque algorithme sélectionné
            for algo_name in algorithms:
                best_solution, best_fitness, exec_time = execute_algorithm(problem, algo_name)
                nb_subsets, covering_rate = display_solution(m, n, k, best_solution, best_fitness, algo_name, exec_time)

                # Sauvegarde des résultats dans une liste
                benchmark_data.append([benchmark_name, algo_name, m, n, k, nb_subsets, best_fitness, covering_rate, exec_time])
            
        # Sauvegarde des résultats dans un fichier CSV
        save_csv(file_path, benchmark_data)
