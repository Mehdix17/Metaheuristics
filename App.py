import streamlit as st
import constants as cst
import dimacs
from fonctions import load_local_graphs, display_op3, path_checker, sort_algo_list, animate
from settings import display_SA_settings, display_GA_settings, display_ACO_settings
from results import run

st.set_page_config(page_title="App", layout="wide")

#------------------------------------ Variables globales --------------------------------------

# dictionnaire des graphes locaux (qui sont sauvegardés dans le workspace)
st.session_state["local_graphs"] = load_local_graphs()

# dictionnaire du graphe créé manuellement
if "created_graph" not in st.session_state:
    st.session_state["created_graph"] = {}

# dictionnaire du graphe créé aléatoirement
if "random_created_graph" not in st.session_state:
    st.session_state["random_created_graph"] = {}

# dictionnaire des paires Graphe / sommet de la 3e opération
if "graph_vertex_dict" not in st.session_state:
    st.session_state["graph_vertex_dict"] = {}

# variable du chemin du Workspace en câs ou on veut modifier le chemin
if "working_directory" not in st.session_state:
    st.session_state["working_directory"] = cst.working_directory_path

#------------------------------------ Variables locales --------------------------------------

# liste des noms des graphe locaux
local_graph_names_list = [graph.name for graph in st.session_state.local_graphs]

# Le dictionnaire des ensembles (graphe / sommet) de l'opération 3
graph_dic = {}

# liste des benchmarks selectionnés par l'utilisateur parmi les 80 disponibles
benchmark_list = []

# liste des graphes locaux selectionnés par l'utilisateur
local_graph_list = []

# variable optionnel pour fixer une limite de temps de calcul
timer = None

#------------------------------------ Home page --------------------------------------

c1, c2 = st.columns([7,3])

with c2:
    animate("Components/data_animation.json", 300, 300)

c1.title("Bienvenue")

# Choix de l'opération
c1.header("Que voulez vous faire ?")
operation = c1.selectbox("_", cst.operations, label_visibility="collapsed")

if operation == cst.operations[2]: # Déterminer La clique maximal relié à un nœud
    graph_dic = display_op3() # affichage différent des deux autres opérations
    
else: # opération 1 ou 2

    c1, c2 = st.columns([7,3])

    with c2:
        animate("Components/graph_animation.json", 250, 250)
    
    # Choix des graphes
    c1.header("Sur quel graphe ?")

    benchmark_name_list = c1.multiselect("Benchmarks", 
                                    dimacs.graph_names_list, 
                                    placeholder="Sélectionnez un ou plusieurs graphes")
    
    # récupérer les benchmarks selectionnés à partir de leurs noms
    benchmark_list = [graph for graph in dimacs.graph_list if graph.name in benchmark_name_list]
    
    local_graph_name_list = c1.multiselect("Graphe locale",
                                    local_graph_names_list, 
                                    placeholder="Sélectionnez un ou plusieurs graphes")
    
    # récupérer les graphes locaux selectionnés à partir de leurs noms
    local_graph_list = [graph for graph in st.session_state.local_graphs if graph.name in local_graph_name_list]

# fusion des 2 listes
graph_list = benchmark_list + local_graph_list

# Choix du ou des algos à appliqués

st.header("")
st.header("Avec quel algorithme ?")
algo_list = st.multiselect("_", 
                           cst.algorithms, 
                            label_visibility="collapsed",
                            placeholder="Veuillez choisir la ou les métaheuristiques à appliquer")

# trier les algos récupérés dans cet ordre : SA - GA - ACO
algo_list = sort_algo_list(algo_list)

# Paramètres
SA_settings = None
GA_settings = None
ACO_settings = None

# fixer les paramètres par défaut des algorithmes seléctionnés selon l'opération choisis
option = 2 if operation == cst.operations[1] else 1

if cst.algorithms[0] in algo_list: # Recuit simulé
    SA_settings = display_SA_settings(option)

if cst.algorithms[1] in algo_list: # Algorithme génétique
    GA_settings = display_GA_settings(option)

if cst.algorithms[2] in algo_list: # Colonies de fourmis
    ACO_settings = display_ACO_settings(option)

# Paramètres optionnels

st.header("")
c1, c2 = st.columns([7,3])

# Ajouter un timer
c1.header("Définir une limite de temps ?")

c3, c4 = c1.columns([1,9])

toggler = c3.toggle("_", label_visibility="hidden")

if toggler:
    timer = c4.slider(label="_", value=30, min_value=1, max_value=300, label_visibility="collapsed")

# Modifier le chemin du workspace
c1.header("Modifier l'espace de travail ?")

c3, c4 = c1.columns([1,9])

toggler = c3.toggle("Modifier", label_visibility="hidden")

if toggler:
    path = c4.text_input(label=",", label_visibility="collapsed", placeholder=st.session_state.working_directory)

    # vérifier que le path saisi est valide
    if path and path_checker(path): 
        st.session_state.working_directory = path
     
with c2:
    animate("Components/settings_animation.json", 300, 300)

# Vérifier que tout est bon avant de lancer les calculs
if operation and algo_list and (graph_list or graph_dic) and (SA_settings or GA_settings or ACO_settings):

    graph_data = graph_list if graph_list else graph_dic
    
    params = (operation, graph_data, algo_list, SA_settings, GA_settings, ACO_settings, timer)
    
    run_button = st.button("Valider", key="run_button")
    
    # Si le bouton est cliqué, lancer l'exécution
    if run_button:
        run(*params)
