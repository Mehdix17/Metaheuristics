import streamlit as st

# chemin du repertoire Bin de la bibliothèque Graphiz
graphiz_bin_path = r"C:\Program Files (x86)\Graphviz\bin"

# Chemin du workspace
working_directory_path = r"C:\Users\mehdi\OneDrive\Bureau\PFE\Programmes\App_V5\Workspace"

if "working_directory" not in st.session_state:
    st.session_state["working_directory"] = working_directory_path

# Noms des 3 opérations
operations = [  "Trouver la clique maximale du graphe", 
                "Localiser toutes les cliques du graphe", 
                "Déterminer la clique maximale reliée à un sommet"
                ]

# Noms des 3 métaheuristiques
algorithms = ["Recuit simulé", "Algorithme génétique", "Colonies de fourmis"]

# Chemins relatifs où sont stockés les résultats dans le workspace
workspace_results_path = ["\Résultats\Clique maximale",
                          "\Résultats\Toutes les cliques",
                          "\Résultats\Clique maximale sommet",
                        ]

# Chemins absolus où sont stockés les résultats dans le workspace
workspace_results_absolute_path = [  st.session_state.working_directory + workspace_results_path[0],
                                    st.session_state.working_directory + workspace_results_path[1],
                                    st.session_state.working_directory + workspace_results_path[2],
                                ]

# Chemins relatifs où sont stockés les graphes locaux dans le workspace
workspace_graphs_path = ["\Graphes\Manuel\JSON",
                          "\Graphes\Manuel\Images",
                          "\Graphes\Aléatoire\JSON",
                          "\Graphes\Aléatoire\Images"
                        ]

# Chemins absolus où sont stockés les graphes locaux dans le workspace
workspace_graphs_absolute_path = [  st.session_state.working_directory + workspace_graphs_path[0],
                                    st.session_state.working_directory + workspace_graphs_path[1],
                                    st.session_state.working_directory + workspace_graphs_path[2],
                                    st.session_state.working_directory + workspace_graphs_path[3],
                                ]
