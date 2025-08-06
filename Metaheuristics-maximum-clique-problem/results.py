import streamlit as st
import constants as cst
from fonctions import load_graph_dic, display_results, display_comparison
from ALGOS import algos

def run(operation, graph_data, algo_list, SA_settings, GA_settings, ACO_settings, timer):

    if operation != cst.operations[2]: # Charger les graphes choisis dans les opérations 1 et 2
        load_graph_dic(graph_data)

    result_list = [] # Liste des résultats de chaque algo appliqué sur chaque graphe
    calcul_time_list = [] # Liste des temps de calcul de chaque algo appliqué sur chaque graphe

    if operation != cst.operations[2]:

        for graph in graph_data:
            result = apply_algo(operation, graph, algo_list, None, SA_settings, GA_settings, ACO_settings, timer)
            result_list.append(result[0])       # Exemple result[0] = (90, 75, 87)
            calcul_time_list.append(result[1])  # Exemple result[1] = (3.4, 6.5, 30)

    else: # Déterminer La clique maximal relié à un nœud

        for graph, vertex in graph_data.items():
            result = apply_algo(operation, graph, algo_list, vertex, SA_settings, GA_settings, ACO_settings, timer)
            result_list.append(result[0])
            calcul_time_list.append(result[1])

    graph_name_list = [graph.name for graph in graph_data] # récupérer les noms des graphes selectionnés

    # Affiche les courbes des différents algorithmes appliqués sur les graphes sélectionnés
    display_comparison(graph_name_list, algo_list, result_list, calcul_time_list, operation)

# fonction qui applique un algo sur un graphe
def apply_algo(operation, graph, algo_list, vertex, SA_settings, GA_settings, ACO_settings, timer):
    
    st.write(f"## Graphe : {graph.name}")
    
    # Initialiser les cliques
    SA_result = None
    GA_result = None
    ACO_result = None

    if operation == cst.operations[0]: # Trouver la clique maximal du graphe

        option = 1
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            st.write(f"Application du {cst.algorithms[0]} ...")
            SA_result = algos.maximum_clique(graph, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            st.write(f"Application de l'{cst.algorithms[1]} ...")
            GA_result = algos.maximum_clique(graph, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
            ACO_result = algos.maximum_clique(graph, ACO_settings, timer, 3)

    elif operation == cst.operations[1]: # Localiser toutes les cliques du graphe

        option = 2
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            st.write(f"Application du {cst.algorithms[0]} ...")
            SA_result = algos.all_clique(graph, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            st.write(f"Application de l'{cst.algorithms[1]} ...")
            GA_result = algos.all_clique(graph, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
            ACO_result = algos.all_clique(graph, ACO_settings, timer, 3)

    else: # Déterminer La clique maximal relié à un nœud

        option = 3
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            st.write(f"Application du {cst.algorithms[0]} ...")
            SA_result = algos.vertex_maximum_clique(graph, vertex, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            st.write(f"Application de l'{cst.algorithms[1]} ...")
            GA_result = algos.vertex_maximum_clique(graph, vertex, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
            ACO_result = algos.vertex_maximum_clique(graph, vertex, ACO_settings, timer, 3)

    # lancer display_results pour afficher les résultats et retouner le résultat et le temps de calcul
    return display_results(graph, vertex, SA_result, GA_result, ACO_result, option)
