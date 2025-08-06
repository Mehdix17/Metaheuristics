import streamlit as st
import pandas as pd
from ALGOS.SA_fonctions import maximum_clique_finder
from fonctions import os, json, get_dot_element, AgGrid
from settings import display_random_graph_settings, animate
import constants as cst
from random import randint

#------------------------------------ Variables globales --------------------------------------

# Variable d'environement nécessaire pour le téléchargement des graphes
os.environ["PATH"] += os.pathsep + cst.graphiz_bin_path

# dictionnaire du graphe créé manuellement
if "created_graph" not in st.session_state:
    st.session_state["created_graph"] = {}

# dictionnaire du graphe créé aléatoirement
if "random_created_graph" not in st.session_state:
    st.session_state["random_created_graph"] = {}
    
#-------------------------------------- Fonctions --------------------------------------

# Télécharge le graphe créé (met les graphes dans les dossiers correspondants)
def download_graph(graph_name, clique_size, dot_element, option):

    if option == 1: # création manuelle
        json_directory = cst.workspace_graphs_absolute_path[0]
        image_directory = cst.workspace_graphs_absolute_path[1]
        graph = st.session_state.created_graph
    
    else: # création aléatoire
        json_directory = cst.workspace_graphs_absolute_path[2]
        image_directory = cst.workspace_graphs_absolute_path[3]
        graph = st.session_state.random_created_graph

    filename = graph_name + ".json"

    # Créer le chemin où sera sauvegardé le graphe
    filepath = os.path.join(json_directory, filename)

    # Vérifier que le nom n'est pas déjà pris
    if os.path.exists(filepath):
        st.toast("Nom de graphe déjà pris", icon="❌")

    else: # créer les fichiers .png et .json
        
        # calculer le nombre d'arrêtes du graphe
        edges = 0 
        for i in graph.values():
            edges += len(i)

        # Créer la structure de données

        data = {
            'name': graph_name,
            'nodes': len(graph.keys()),
            'edges': edges,
            'clique_size': clique_size,
            'graph_dic': graph
        }

        # Partie fichier .json

        with open(filepath, 'w', newline='') as f:
            json.dump(data, f)
        
        # Partie fichier .png
        
        dot_element.render(directory = image_directory, 
                            filename=graph_name, 
                            format="png", 
                            cleanup=True)
        
        st.toast("Graphe ajouté avec succès", icon="✅")

#------------------------- Fonctions pour la création manuelle de graphes -----------------------------

# Pour ajouter un sommet et ses voisins
def add_vertex_func(sommet_val, voisin_list):

    # Récupérer la liste des clés du graphe en cours de création
    dic_keys = list(st.session_state.created_graph.keys())

    # Ajouter le sommet et ses voisins au graphe
    st.session_state.created_graph[sommet_val] = voisin_list
    
    # Parcourir la liste des voisins
    for v in voisin_list:

        # Ajouter le sommet dans la liste des voisins de ses voisins
        if v not in dic_keys: 
            st.session_state.created_graph[v] = [sommet_val]

        # Si l'un des voisins du sommet ajouté n'existe pas encore, l'ajouter
        else:
            if sommet_val not in st.session_state.created_graph[v]:
                st.session_state.created_graph[v].append(sommet_val)

    # faire la mise à jour dans le càs où on a changé la liste des voisins d'un sommet
    for i, j in st.session_state.created_graph.items():
        for k in j:
            if i not in st.session_state.created_graph[k]:
                j.remove(k)

# Pour Supprimer un sommet
def del_vertex_func(sommet_val):

    # Commencer par vérifier que le sommet existe bien dans le graphe
    if sommet_val in st.session_state.created_graph:

        # Récupérer la liste des voisins du sommet
        neighbors = st.session_state.created_graph[sommet_val]

        # Supprimer le sommet de la liste des voisins de ses voisins
        for neighbor in neighbors:
            st.session_state.created_graph[neighbor].remove(sommet_val)

        # Supprimer le sommet
        del st.session_state.created_graph[sommet_val]
    
    else:
        st.toast(f"{sommet_val} n'existe pas dans le graphe, impossible de le supprimer", icon="❌")

#--------------------------- Fonctions pour la création aléatoire de graphes -------------------------------

def generate_random_graph(vertices, edges):

    # Initialiser le graphe
    graph_dict = {i: [] for i in range(1, vertices + 1)}

    # Créer les arrêtes aléatoirement en évitant les duplication et les boucles
    
    while edges > 0:
        vertex1 = randint(1, vertices)
        vertex2 = randint(1, vertices)
        
        if vertex1 != vertex2 and vertex2 not in graph_dict[vertex1]:
            graph_dict[vertex1].append(vertex2)
            graph_dict[vertex2].append(vertex1)
            edges -= 1

    # Trier le graphe
    graph_dict = dict(sorted(graph_dict.items()))
    st.session_state.random_created_graph = graph_dict

#------------------------------------ Création manuelle des graphes ---------------------------------------

st.markdown("# Graphes locaux")

st.markdown("## Créer un graphe manuellement")

# variable pour stocker la clique maximale qui sera calculé dès que le graphe sera créé
maximum_clique = None

# Liste des sommets disponibles (entre 1 et 100)
vertex_list = list(i for i in range(1, 101))

c1, c2, c3 = st.columns([2,2,6])

# Choix du nom du graphe
graph_name = c1.text_input("Entrez le nom du graphe : ")

# Choix du sommet
vertex_val = int(c2.selectbox(label="Choisir un sommet", options=vertex_list))

# Supprimer le sommet de la liste des voisins
tempo_list = vertex_list.copy()
tempo_list.remove(vertex_val)

# Récupérer la liste des voisins
voisins_list = c3.multiselect(label="Ajouter les voisins", 
                                options=tempo_list, 
                                placeholder="Liste des voisins")

c1, c2, c3, c4 = st.columns(4)

# Création des boutons
add_vertex_button = c1.button("Ajouter sommet")
delete_vertex_button = c2.button("Supprimer sommet")
reset_graph_button = c3.button("Rénitialiser graphe")

# Déclenchement des fonctions si les boutons sont cliqués

if add_vertex_button:
    add_vertex_func(vertex_val, voisins_list)
    vertex_list = [s for s in range(1, 101) if s not in st.session_state.created_graph.keys()]

if delete_vertex_button:
    del_vertex_func(vertex_val)

if reset_graph_button:
    st.session_state.created_graph.clear()

if st.session_state.created_graph:
    maximum_clique, _ = maximum_clique_finder(st.session_state.created_graph, 1500, 0.99, 1000, None)

# Trier le graphe créé
sorted_created_graph = dict(sorted(st.session_state.created_graph.items()))

# Créer le DataFrame
df = pd.DataFrame(sorted_created_graph.items(), columns=['Sommet', 'Voisins'])

# Convertir les éléments uniques en listes
df['Voisins'] = df['Voisins'].apply(lambda x: [x] if not isinstance(x, list) else x)

# Trier la liste des voisins
df['Voisins'] = df['Voisins'].apply(lambda x: sorted(x))

c1, c2 = st.columns([3,7])

# Affichage du tableau Sommet/Voisins
with c1:
    AgGrid(df, fit_columns_on_grid_load=True, height=400)

# Récupérer l'objet dot du graphe créé
dot_element = get_dot_element(sorted_created_graph, None)

# Afficher le graphe
with c2:
    st.graphviz_chart(dot_element)

# Si tous est bon afficher le bouton de téléchargement
if graph_name and maximum_clique:
    download_graph_button = c4.button("Télécharger graphe", 
                                        on_click=download_graph, 
                                        args=(graph_name, len(maximum_clique), dot_element, 1))

st.write(f"### La clique maximale : {maximum_clique}")

#------------------------------------ Création aléatoire de graphes ----------------------------------------

st.header("")
st.markdown("## Créer un graphe aléatoirement")

c1, c2 = st.columns([7,3])

with c2:
    animate("Components/algo_animation.json", 300, 300)

with c1:
    
    # Choix du nom du graphe
    random_graph_name = st.text_input("Entrez le nom du graphe : ", key="random_graph_name")

    # Choix du nombre de sommets et arrêtes
    vertice_number, edges_number = display_random_graph_settings(random_graph_name)

# Si tout est bon lancer le processus de création du graphe
if random_graph_name and vertice_number and edges_number:

        directory = cst.workspace_graphs_absolute_path[2]
        filename = random_graph_name + ".json"
        filepath = os.path.join(directory, filename)
        
        # Si le chemin n'existe pas, générer le graphe et calculer la clique maximale
        if not os.path.exists(filepath):

            generate_random_graph(vertice_number, edges_number)
            maximum_clique, _ = maximum_clique_finder(st.session_state.random_created_graph, 1500, 0.99, 1000, None)
            
            # récupérer l'objet dot
            dot_element = get_dot_element(st.session_state.random_created_graph, None)

            # Afficher le graphe et la clique maximale
            st.graphviz_chart(dot_element)
            st.write(f"### La clique maximale : {maximum_clique}")
            
            # Sauvegarde du graphe dans le Workspace
            download_graph(random_graph_name, len(maximum_clique), dot_element, 2)
        
        else:
            st.toast("Nom de graphe déjà pris", icon="❌")
