import os
import math

def parse(file_path):

    with open(file_path, "r") as file:
        m, n = map(int, file.readline().split()) # lecture de la première ligne

        # Calcul de k (nombre de subsets à sélectionner) : 2/3 de m
        k = math.ceil((2/3) * m)  # Arrondi au supérieur

        # Liste des subsets
        subsets = []

        # Read the Subset Coverage Details
        for _ in range(m):
            while True:
                line = file.readline().strip()
                if line.isdigit():  # We found the number of covered elements
                    num_elements = int(line)
                    break  # Stop looking for the header
            
            subset = []  # List to store covered elements
            
            # Read elements, handling cases where they span multiple lines
            while len(subset) < num_elements:
                subset.extend(map(int, file.readline().split()))

            subsets.append(subset)

    return subsets, m, n, k

def parse_all_benchmarks(benchmark_dir):
    all_instances = []  # Liste pour stocker toutes les instances

    # Parcourir les sous-dossiers de `benchmark_dir`
    for subdir in os.listdir(benchmark_dir):
        subdir_path = os.path.join(benchmark_dir, subdir)
        
        # Vérifier que c'est bien un dossier
        if os.path.isdir(subdir_path):
            
            # Parcourir tous les fichiers du sous-dossier
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)

                # Vérifier que c'est un fichier
                if os.path.isfile(file_path):
                    try:
                        # Extraire le nom du benchmark sans l'extension .txt
                        benchmark_name = os.path.splitext(filename)[0]

                        # Parser le fichier benchmark
                        subsets, m, n, k = parse(file_path)

                        # Ajouter à la liste avec le nom du benchmark
                        all_instances.append([benchmark_name, (subsets, m, n, k)])
                    
                    except Exception as e:
                        print(f"❌ Erreur lors du parsing de {file_path} : {e}")

    return all_instances
