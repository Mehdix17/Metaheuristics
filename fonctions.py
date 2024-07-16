import streamlit as st
import constants as cst
import pandas as pd
import plotly.express as px
import dimacs, json, os, graphviz, csv, time, datetime
from streamlit_lottie import st_lottie
from collections import Counter
from random import choice
from st_aggrid import AgGrid

#------------------------------------ Fonctions gestion des graphes ------------------------------------

# fontion qui charge tous les les graphes qui se trouvent dans le Workspace
def load_local_graphs():
    
    # Liste qui va contenir les graphes locaux
    local_graphs = []
    manual_graph_list = []
    random_graph_list = []

    # Charger les grahpes locaux
    manual_graph_list = get_graph_from_path(cst.workspace_graphs_absolute_path[0])
    random_graph_list = get_graph_from_path(cst.workspace_graphs_absolute_path[2])

    # Fusioner les 2 listes
    graph_list = manual_graph_list + random_graph_list

    # Créer l'objet Graph
    for graph in graph_list:

        new_graph = dimacs.Graph(graph['name'], 
                                graph['nodes'], 
                                graph['edges'], 
                                graph['clique_size'], 
                                graph['graph_dic'],
                                None)
        
        local_graphs.append(new_graph)

    return local_graphs

# Fonction qui récupère tous les fichiers .json d'un répertoire 
def get_graph_from_path(path):

    graph_list = []

    for filename in os.listdir(path):
        tempo_graph = {}

        filepath = os.path.join(path, filename)
        
        if os.path.isfile(filepath):

            with open(filepath, "r") as file:
                graph_object = json.load(file)

            # convertir les clés du graph_dict en int car elle sont string à cause du json.dump()
            for k, v in graph_object['graph_dic'].items():
                tempo_graph[int(k)] = v
            graph_object['graph_dic'] = tempo_graph

            graph_list.append(graph_object)

    return graph_list

# fonction pour charger les graphes sélectionnés
def load_graph_dic(graph_list):
    for graph in graph_list:
        if not graph.graph_dic:
            set_graph_dic(graph)

# Fonction pour charger le dictionnaire des Benchmakrs DIMACS
def set_graph_dic(graph):
    graph_dic = {}
    with open(graph.file_path, 'r') as f:
        for line in f:
            if line.startswith('e'):
                _, u, v = line.split()
                u, v = int(u), int(v)
                if u not in graph_dic:
                    graph_dic[u] = []
                if v not in graph_dic:
                    graph_dic[v] = []
                graph_dic[u].append(v)
                graph_dic[v].append(u)
    graph.graph_dic = graph_dic

# fontion pour dessiner un graphe
def get_dot_element(graph_dict, vertex_to_color):
    
    dot = graphviz.Graph()  # Utiliser la classe Graph pour un graphe non orienté
    sorted_dict = {key: graph_dict[key] for key in sorted(graph_dict.keys())}

    for vertex, neighbors in sorted_dict.items():

        if vertex_to_color:
            
            if vertex != vertex_to_color:
                dot.node(str(vertex))
            else:
                node_style = {'color': 'red', 'style': 'filled'}
                dot.node(str(vertex), _attributes=node_style)
         
        if neighbors:

            for neighbor in neighbors:
                
                # Ajouter des arêtes seulement si le nœud actuel est plus petit que le voisin
                    if vertex < neighbor:
                        dot.edge(str(vertex), str(neighbor))
            
        else: # dessiner le sommet isolé
            dot.node(str(vertex))

    return dot    

# pour créer des graphes à partir des cliques obtenues
def create_graph_from_clique(clique):
    graph_dic = {}
    for i in clique:
        graph_dic[i] = [v for v in clique if v != i]
    return graph_dic

#------------------------------------ Fonctions affichage des résultats ------------------------------------

# Fonction principale pour l'affichage des résultats, retourne les résultats et temps de calcul obtenus
def display_results(graph, vertex, SA_clique, GA_clique, ACO_clique, option):

    algo_list = [] # liste des noms des algos appliqués
    clique_list = [] # liste des cliques trouvées par les différents algos
    calcul_time_list = [] # liste des temps de calcul pour chaque algo

    # Création du répertoire de l'opération
    directory_name = directory_maker(graph, option)

    # Affichage des résultats obtenus par chaque algorithme

    if SA_clique: # Recuit simulé
        display_clique(SA_clique, algo_list, clique_list, calcul_time_list, vertex, directory_name, 0, option)
    
    if GA_clique: # Alogirhtme génétique
        display_clique(GA_clique, algo_list, clique_list, calcul_time_list, vertex, directory_name, 1, option)
    
    if ACO_clique: # Colonie de fourmis
        display_clique(ACO_clique, algo_list, clique_list, calcul_time_list, vertex, directory_name, 2, option)
    
    # Affichage des diagrammes récapitulatifs et récupération des résultats
    result_list = display_bar_charts(graph, algo_list, clique_list, calcul_time_list, option)

    return [result_list, calcul_time_list]

# Affiche le résultat obtenu par un algorihtme sur un graphe
def display_clique(clique, algo_list, clique_list, calcul_time_list, vertex, directory_name, index, option):

    # Ajouter le nom de l'algo à algo_list
    algo_name = cst.algorithms[index]
    algo_list.append(algo_name)
    
    # Ajouter le résultat obtenu par l'algo à clique_list
    clique_list.append(clique[0])

    # Ajouter le temps de calcul de l'algo à calcul_time_list
    calcul_time_list.append(clique[1])
    
    # Affichage des résultats
    st.write(f"## Résultat {algo_name}")
    
    if option in (1,3): # opération 1 ou 3
        
        if option == 1:
            st.markdown(f"### Clique trouvée : {clique[0]}")
        
        else:
            st.markdown(f"### La clique maximale relié à {vertex} : {clique[0]}")

        st.write("### Taille de la clique : ", len(clique[0]))
        
        st.write("### Temps de calcul : ", clique[1], "s")

        # Affichage de la clique trouvé si sa taille est inférieur à 50

        if len(clique[0]) < 50:

            # convertir la clique obtenue en dictionnaire
            graph_dic = create_graph_from_clique(clique[0])
            
            # Récupérer l'objet de type dot pour l'afficher
            dot_element = get_dot_element(graph_dic, vertex)

            # Sauvegarder le graphe dans le Workspace
            dot_element.render(directory = directory_name, 
                                filename=algo_name, 
                                format="png", 
                                cleanup=True)
            
            st.toast("Graphe ajouté avec succès", icon="✅")

            # Dessiner le graphe
            st.graphviz_chart(dot_element)
        
        else: # l'image va être trop voluminuese, elle ve prendre trop de temps à s'afficher et à sauvegarder
            st.image("Components\Images\error.png", width=200)
    
    else: # Traitement différent pour l'opération 2

        st.write("### Nombre de cliques trouvées : ", len(clique[0]))
        st.write("### Temps de calcul : ", clique[1], "s")

        # Sauvegarder dans le Workspace toutes les cliques trouvées sous forme de fichier CSV
        csv_file_generator(directory_name, algo_name, clique[0])

        # Afficher le diagramme circulaire
        display_pie_chart(clique[0])

# Génère un fichier CSV contenant toutes les cliques trouvées
def csv_file_generator(directory_name, algo_name, all_cliques):

    # Créer le repertoire la première fois
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # Création du chemin du fichier
    filename = algo_name + ".csv"
    filepath = os.path.join(directory_name, filename)
    
    # Écriture sur le fichier CSV
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for clique in all_cliques:
            writer.writerow(list(clique))

    st.toast(f"Cliques trouvées par {algo_name} sauvegardées avec succès", icon="✅")

# Affiche le diagramme circulaire (camembert)
def display_pie_chart(all_cliques):

    # Récupérer un objet Counter qui contient un dictionnaire de (taille clique / occurence)
    clique_size_counts = Counter(len(clique) for clique in all_cliques)
    
    # Trier le dictionnaire dans l'ordre des tailles des cliques
    clique_size_counts = dict(sorted(clique_size_counts.items()))

    # Calculer les pourcentage de chaque taille de clique et les stockés dans un dictionnaire
    clique_size_percentages = {size: (count / len(all_cliques)) * 100 for size, count in clique_size_counts.items()}

    # Créer un dictionanire qui contient les messages "Clique de taille = taille" pour chaque taille de clique
    size_ranges = {}
    for i in clique_size_counts:
        size_ranges[i] = f"Clique de taille = {i}"

    # Créer un dictionnaire finale de la forme (Clique de taille = taille/pourcentage) qui sera passé comme
    # paramètre à la fonction px.pie() qui crééra le diagramme circulaire
    
    pie_dict = {
        "Taille" : [],
        "pourcentage" : []
    }

    # Remplir le dictionnaire 
    for size, count in clique_size_percentages.items():
        if size in size_ranges:
            pie_dict["Taille"].append(size_ranges[size])
            pie_dict["pourcentage"].append(count)

    # création du diagramme circulaire
    fig = px.pie(pie_dict, values="pourcentage", names="Taille")
    st.plotly_chart(fig)

# Affiche les diagrmmes en batôns comparatifs
def display_bar_charts(graph, algo_list, clique_list, calcul_time_list, option):

    # résultats retournés pour les opération 2 et 3 et c'est aussi la valeur sur l'axe des ordonnées
    clique_size_list = [len(clique) for clique in clique_list]

    if option == 1:
        # résultats retournés pour l'opération 1 et c'est aussi la valeur sur la colonne "Efficacité %"
        efficiency_list = [round(e/graph.clique_size*100, 2) for e in clique_size_list]

    if len(algo_list) > 1: # Afficher les diagrammes comparatifs s'il y'a au moins deux algos

        if option == 1: # Traitement spécial pour l'opération 1 (le tableau récapitulatif)
            
            y_string = "Taille de la clique" # variable du String sur l'axe des ordonnées du diagramme

            # Création du DataFrame
            table_df = pd.DataFrame({
                "Algorithmes": algo_list,
                "Clique trouvée": clique_list,
                "Taille de la clique": clique_size_list,
                "Temps de calcul": calcul_time_list,
                "Efficacité %" : efficiency_list
            })

            # Création du tableau
            st.write("## Tableau récapitulatif")
            AgGrid(table_df, fit_columns_on_grid_load=True, height=30*len(clique_list) + 30)
        
        elif option == 2:
            y_string = "Nombre de cliques trouvées" 
        
        else:
            y_string = "Taille de la clique"

        # Traitement spécial pour l'opération 1 (ajouter l'optimum global)
        new_clique_size_list = clique_size_list + [graph.clique_size] # Les barres sur le graphique
        new_algo_list = algo_list + ["Optimum global"] # Les noms des algos sur l'axe des abscisses
        
        # diagramme en bâtons des cliques trouvées

        # Création du DataFrame
        chart_df = pd.DataFrame({
            "Algorithmes": new_algo_list if option == 1 else algo_list,
            y_string: new_clique_size_list if option == 1 else clique_size_list
        })

        # Affichage du diagramme
        st.write(f"## {y_string}")
        fig = px.bar(chart_df, x='Algorithmes', y=y_string, color="Algorithmes")
        st.plotly_chart(fig, use_container_width=True)

        # diagramme en bâtons des temps de calcul

        # Création du DataFrame
        chart_df = pd.DataFrame({
            "Algorithmes": algo_list,
            "Temps de calcul": calcul_time_list
        })

        # Affichage du diagramme
        st.write("## Temps de calcul")
        fig = px.bar(chart_df, x='Algorithmes', y='Temps de calcul', color="Algorithmes")
        st.plotly_chart(fig, use_container_width=True)
    
    return clique_size_list if option != 1 else efficiency_list

# Affiche les courbes des différents algorithmes appliqués sur les graphes sélectionnés
def display_comparison(graph_name_list, algo_list, result_list, calcul_time_list, operation):

    if operation == cst.operations[0]: # Trouver la clique maximale du graphe
        y_string = "Efficacité"

    elif operation == cst.operations[1]: # Localiser toutes les cliques du graphe
        y_string = "Nombre de cliques"
    
    else: # Déterminer La clique maximal reliée à un sommet
        y_string = "Taille de la clique maximale"
    
    # Affiche les courbes des résultats obtenus pour chaque algo
    display_line_chart(graph_name_list, algo_list, result_list, y_string, "Résumé des résultats")
    
    # Affiche les courbes des temps de calculs pour chaque algo
    display_line_chart(graph_name_list, algo_list, calcul_time_list, "Temps de calcul", "Résumé des temps de calcul")

# pour afficher les courbes
def display_line_chart(graph_name_list, algo_list, result_list, y_string, title_string):

        st.markdown(f"# {title_string}")
        data = [] # liste des résultats, chaque élément est de la forme : (graphe, algorithme, résultat)
        
        # Remplissage de la liste data 
        for i, graph_name in enumerate(graph_name_list):
            for j, algo in enumerate(algo_list):
                data.append({"Graphes": graph_name, "Algorithmes": algo, y_string: result_list[i][j]})

        # Création du DataFrame
        line_chart_frame = pd.DataFrame(data)

        # Affichage de la courbe
        fig = px.line(line_chart_frame, x="Graphes", y=y_string, color="Algorithmes", markers=True)
        st.plotly_chart(fig, use_container_width=True)

#------------------------------------ Autres Fonctions ------------------------------------

# pour les animations
@st.cache_resource(experimental_allow_widgets=True) # pour l'optimisation
def animate(file_path, widget_height, widget_width):
    with open(file_path, 'r') as f:
        animation_data = json.load(f)
        st_lottie(animation_data, height=widget_height, width=widget_width)

# trie les algos selectionnés par l'utilisateur dans cet ordre : SA - GA - ACO
def sort_algo_list(algo_list):
    tempo_list = []
    for algo in cst.algorithms:
        if algo in algo_list:
            tempo_list.append(algo)
    return tempo_list

# Vérifie que le nouveau chemin du workspace est valide
def path_checker(path):

    if len(path) > 2 and (path[0] and ("C:", "D:", "E", "F", "G") and path[1] == ":" and path[2] == "\\"):

        if os.path.exists(path): # vérifier l'existence du chemin
            path_exists = True
        
        else: # si le chemin n'existe pas, on essaye de le créer
            
            try:
                os.makedirs(path)
                path_exists = True
            
            except OSError: # En cas d'echec de la création, afficher un message d'erreur
                st.toast("Une erreur est survenue", icon="❌")
                return False
            
        if path_exists: # vérifier maintenant les sous-répertoires
            
            # récupérer les paths des sous-répertoires
            workspace_paths = cst.workspace_results_path + cst.workspace_graphs_path

            # Vérifier et créer les sous-répertoires s'il n'existe pas
            for relative_path in workspace_paths:
                if not os.path.exists(path + relative_path):
                    os.makedirs(path + relative_path)

            st.toast("Espace de travail mise à jour", icon="✅")
            return True

    else: # le chemin entré par l'utilisateur est invalide
        st.toast(f"Le chemin d'accès '{path}' est invalide", icon="❌")
        return False

# pour créer le répertoire qui stockera les résultats obtenus par chaque opérations
def directory_maker(graph, option):
    
    date_id = "\\" + datetime.date.today().strftime(r"%d-%m-%Y") # récupérer la date du jour
    
    current_time = time.localtime() # récupérer l'heure exacte
    time_id = " ({})".format(time.strftime("%Hh %Mm %Ss", current_time)) # formater l'heure

    # Créer le répertoire
    directory_name = cst.workspace_results_absolute_path[option-1] + date_id + f"\{graph.name}" + time_id 

    # Exemple de repertoire : C:\Users\mehdi\OneDrive\Bureau\PFE\Programmes\App_V5\Workspace\Résultats
                              # \Clique maximale\27-05-2024\brock200_1 (18h 48m 56s)    
    return directory_name

# Affichage différent pour l'opération 3
def display_op3():

    # liste de tous les graphes (benchmarks + locaux)
    graph_list = dimacs.graph_list + st.session_state.local_graphs

    # liste des noms de tous les graphes
    graph_name_list = [graph.name for graph in graph_list]

    st.markdown("# Associez à chaque graphe un sommet")

    column1, column2 = st.columns([7,3])

    c1, c2 = column1.columns(2)
    
    # Choix du graphe
    graph_name = c1.selectbox(label="Choisir un graphe", options=graph_name_list)

    # Récupérer le graphe
    graph_item = [graph for graph in graph_list if graph.name == graph_name][0]

    # Charger le dictionnaire du graphe s'il n'est pas chargé
    if not graph_item.graph_dic:
        set_graph_dic(graph_item)

    # liste des sommets non isolés
    tempo_list = sorted([i for i,j in graph_item.graph_dic.items() if j])  
    
    # Choix du sommet
    vertex_item = c2.selectbox(label="Choisir un sommet", options=tempo_list)

    # Création des boutons
    c1, c2, c3, c4 = column1.columns(4)
    add_button = c1.button("Ajouter")
    delete_button = c2.button("Supprimer")
    random_vertex_button = c3.button("Aléatoire")
    reset_button = c4.button("Rénitialiser")

    if add_button: # Ajouter la paire graphe/sommet
        
        if not graph_item:
            st.toast('Veuillez séléctionner un graphe', icon='❌')
        
        elif not vertex_item:
            st.toast('Veuillez séléctionner un sommet', icon='❌')
        
        else:
            st.session_state.graph_vertex_dict[graph_item] = vertex_item
            st.toast('Ajout avec succès', icon="✅")
    
    if delete_button: # Supprimer la paire graphe/sommet

        if graph_item not in st.session_state.graph_vertex_dict.keys():
            st.toast('Graphe non séléctionné, impossible de le supprimer', icon='❌')

        else:
            del st.session_state.graph_vertex_dict[graph_item]
            st.toast('Suppression avec succès', icon="✅")

    if random_vertex_button: # Ajouter aléatoirement une paire graphe/sommet
        
        graph_item = choice([graph for graph in graph_list if graph not in st.session_state.graph_vertex_dict.keys()])
        
        if not graph_item.graph_dic:
            set_graph_dic(graph_item)
        
        vertex_item = choice(list(graph_item.graph_dic.keys()))
        st.session_state.graph_vertex_dict[graph_item] = vertex_item

    if reset_button: # Vider le graphe
        st.session_state.graph_vertex_dict.clear()

    # Créer le DataFrame du tableau contenant toutes les paires graphe/sommet selectionnées
    graph_name_list = [graph.name for graph in st.session_state.graph_vertex_dict.keys()]
    
    df = pd.DataFrame({"Graphe" : graph_name_list,
                      "Sommet" : st.session_state.graph_vertex_dict.values()})
        
    # Affichage du tableau 

    with column1:
        AgGrid(df, fit_columns_on_grid_load=True, height=150)

    with column2:
        animate("Components/associate.json", 300, 300)

    return st.session_state.graph_vertex_dict
