import random
import datetime
import time
import csv
import os
import utils.constants as cst
import utils.art as art
from algorithms.dfs import DepthFirstSearch
from algorithms.genetic import GeneticAlgorithm

#--------------------------------------- Affiche le menu principal ---------------------------------

def display_menu():
    print(art.MENU)
    answer = input("\nVotre réponse : ")
    
    # l'utilisateur a entré le numéro d'un benchmark
    if answer.isdigit():
        instance_list = [cst.BENCHMARKS[int(answer)-1]] # liste contenant un seul benchmark
        print(art.ALGO_MENU)
        algo_code = int(input("\nVotre réponse : ")) # 1 = Génétique, 2 = DFS, 3 = les deux
        return instance_list, algo_code
    
    # l'utilisateur a entré 'random'
    elif answer == "random":
        n = int(input("\nEntrer le nombre d'instances : "))
        instance_list = random.sample(cst.BENCHMARKS, n) # liste contenant n benchmarks
        print(art.ALGO_MENU)
        algo_code = int(input("\nVotre réponse : ")) # 1 = Génétique, 2 = DFS, 3 = les deux
        return instance_list, algo_code
    
    # l'utilisateur a entré 'benchmarks'
    elif answer == "benchmarks":
        print(art.BENCHMARKS_TABLE)
        return None, None
    
    else:
        exit()

#--------------------------------------- execute l'algorithme choisi ---------------------------------

def execute_algorithm(problem, algo_name):
     
    if algo_name == cst.ALGOS[0]:
        solver = GeneticAlgorithm(problem)
    else:
        solver = DepthFirstSearch(problem, 10) # 10s pour la démonstration

    print(f"\nExécution de l'algorithme {algo_name} ...")
    best_solution, best_fitness, exec_time = solver.run()
    return best_solution, best_fitness, exec_time

#------------- Affiche la solution finale et sauvegarde le résultat dans un fichier .csv -------------

def display_solution(m, n, k, best_solution, best_fitness, algo_name, exec_time):
    
    print(f"\n******************************* {algo_name} *******************************")
    
    print(f"\nLes subsets selectionnés : {sorted(best_solution)}")

    # Nombre de subsets
    print(f"\n🔴 Nombre de subset total (m) = {m}")
    print(f"\n🔴 Nombre d'éléments total (n) = {n}")
    print(f"\n🔴 Nombre de subset voulu (k) = {k}")
    
    # Nombre d'éléments
    nb_subsets = len(best_solution)
    print(f"\n🟢 Nombre de subset de la solution = {nb_subsets}")

    print(f"\n🟢 Nombre d'éléments couverts = {best_fitness}")
    
    # Taux de couverture
    covering_rate = round((best_fitness/n)*100, 2)
    print(f"\n🟢 Taux de couverture = {covering_rate} %")

    print(f"\n⏱️  Temps d'exécution = {exec_time} s")

    # Vérifier la validité de la solution (nb_susbsets == k ?)
    check_validity(nb_subsets, k)

    return nb_subsets, covering_rate

#--------------------------------------- vérifie la validité de la solution ---------------------------------

def check_validity(nb_subsets, k):
    if nb_subsets == k:
        print("\n✅ Nombre de subset de la solution = k, la solution est donc valide")
    else:
        print("\n❌ Nombre de subset de la solution != k, la solution est donc invalide")

#--------------------------------------- créer un fichier .csv ---------------------------------

def file_maker():
    date_id = datetime.date.today().strftime(r"%d-%m-%Y") # récupérer la date du jour
    current_time = time.localtime() # récupérer l'heure exacte
    time_id = "_{}".format(time.strftime("%Hh-%Mm-%Ss", current_time)) # formater l'heure
    filename =  date_id + time_id + ".csv" # Créer le fichier

    # Assurer que le répertoire existe
    os.makedirs(cst.HISTORY_PATH, exist_ok=True)

    # Construire le chemin complet du fichier
    file_path = os.path.join(cst.HISTORY_PATH, filename)
    
    return file_path

#------------------------------ enregistre les résultats dans un fichier .csv ------------------------

def save_csv(file_path, data):

    # Écriture dans le fichier CSV
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Écrire l'en-tête
        writer.writerow(["Benchmark", "Algorithme", "m", "n", "k", "Nb_Subsets_Solution", "Elements_Couverts", "Taux_Couverture (%)", "Temps d'execution"])

        # Ajouter la ligne des résultats
        for row in data:
            writer.writerow(row)

    print(f"\n✅ Résultats sauvegardés dans `{file_path}`")
