import streamlit as st
from fonctions import animate
from random import choice

# Affichage des paramètres de recuit simulé
def display_SA_settings(option):

    st.header("Paramètres du recuit simulé")

    # slider's keys
    SA_key1 = 1
    SA_key2 = 10000
    SA_key3 = 20000

    # maximum clique values
    maximum_clique_values = [1500, 0.99, 10000]
    maximum_clique_max_values = [3000, 0.99, 5000]

    # all cliques values
    all_cliques_values = [500, 0.99, 1000000]
    all_cliques_max_values = [3000, 0.99, 1000000]
    
    # values lists
    values_list = maximum_clique_values if option == 1 else all_cliques_values
    max_values_list = maximum_clique_max_values if option == 1 else all_cliques_max_values

    c1, c2 = st.columns([7,3])

    with c1:

        # Sliders components
        SA_slider_place_holder1 = st.empty()
        SA_slider_place_holder2 = st.empty()
        SA_slider_place_holder3 = st.empty()
        
        # Sliders

        SA_s1 = SA_slider_place_holder1.slider(label="Température initiale", 
                                            min_value=1, 
                                            max_value=max_values_list[0], 
                                            value=values_list[0], 
                                            key=SA_key1)

        SA_s2 = SA_slider_place_holder2.slider(label="Taux de refroidissement", 
                                            min_value=0.01, 
                                            max_value=max_values_list[1], 
                                            value=values_list[1], 
                                            step=0.01,
                                            key=SA_key2)
        
        SA_s3 = SA_slider_place_holder3.slider(label="Nombre d'itération", 
                                            min_value=1, 
                                            max_value=max_values_list[2], 
                                            value=values_list[2], 
                                            key=SA_key3)

    with c2:
        animate("Components/Thermometer.json", 300, 300)
        
    c3, c4 = c1.columns(2)
    
    with c3:
        SA_reset_button = st.button(label="Rénitialiser", key="SA_reset_button")
    
    with c4:
        SA_random_button = st.button(label="ajuster aléatoirement", key="SA_random_button")

    #  Pour Rénitialiser les paramètres ou les ajustés aléatoirement
    def change_settings(reset_iteration=1, option=0): 

        SA_slider_place_holder1.empty()
        SA_slider_place_holder2.empty()
        SA_slider_place_holder3.empty()

        if option == 1: # Rénitialiser paramètres
            values = values_list

        else: # option = 2 : ajuster les paramètres aléatoirement

            values = [choice(range(1, max_values_list[0])),
                    choice(range(1, int(max_values_list[1]*100)+1)) / 100,
                    choice(range(1, max_values_list[2]))
            ]
        
        s1 = SA_slider_place_holder1.slider(label="Température initiale",
                                            min_value=1, 
                                            max_value=max_values_list[0], 
                                            value=values[0], 
                                            key=SA_key1+reset_iteration)
                
        s2 = SA_slider_place_holder2.slider(label="Taux de refroidissement",
                                            min_value=0.01, 
                                            max_value=max_values_list[1], 
                                            value=values[1], 
                                            step=0.01, 
                                            key=SA_key2+reset_iteration)
        
        s3 = SA_slider_place_holder3.slider(label="Nombre d'itération",
                                            min_value=1, 
                                            max_value=max_values_list[2], 
                                            value=values[2], 
                                            key=SA_key3+reset_iteration)
        return s1, s2, s3

    if SA_reset_button:
        SA_reset_button += 1
        SA_s1, SA_s2, SA_s3 = change_settings(SA_reset_button, 1)

    if SA_random_button:
        SA_reset_button += 1
        SA_s1, SA_s2, SA_s3 = change_settings(SA_random_button, 2)

    return [SA_s1, SA_s2, SA_s3]

# Affichage des paramètres de l'algorithme génétique
def display_GA_settings(option):

    st.header("Paramètres de l'algorithme génétique")

    # slider's keys
    GA_key1 = 30000
    GA_key2 = 40000
    GA_key3 = 50000
    GA_key4 = 60000

    # maximum clique values
    maximum_clique_values = [10, 0.1, 0.8, 1000]
    maximum_clique_max_values = [100, 0.99, 0.99, 2000]

    # all cliques values
    all_cliques_values = [10000, 0.99, 0.99, 100000]
    all_cliques_max_values = [10000, 0.99, 0.99, 100000]
    
    # values lists
    values_list = maximum_clique_values if option == 1 else all_cliques_values
    max_values_list = maximum_clique_max_values if option == 1 else all_cliques_max_values

    c1, c2 = st.columns([7,3])

    with c1:

        # Sliders components
        GA_slider_place_holder1 = st.empty()
        GA_slider_place_holder2 = st.empty()
        GA_slider_place_holder3 = st.empty()
        GA_slider_place_holder4 = st.empty()

        # Sliders
        GA_s1 = GA_slider_place_holder1.slider(label="Taille de la population initiale", 
                                                min_value=1, 
                                                max_value=max_values_list[0], 
                                                value=values_list[0], 
                                                key=GA_key1)

        GA_s2 = GA_slider_place_holder2.slider(label="Taux de mutation", 
                                                min_value=0.01, 
                                                max_value=max_values_list[1], 
                                                value=values_list[1], 
                                                step=0.01, 
                                                key=GA_key2)

        GA_s3 = GA_slider_place_holder3.slider(label="Taux de croisement", 
                                                min_value=0.01, 
                                                max_value=max_values_list[2], 
                                                value=values_list[2], 
                                                step=0.01,  
                                                key=GA_key3)

        GA_s4 = GA_slider_place_holder4.slider(label="Nombre de générations", 
                                                min_value=1, 
                                                max_value=max_values_list[3], 
                                                value=values_list[3], 
                                                key=GA_key4)

    with c2:
        animate("Components/genetic_animation.json", 400, 400)

    c3, c4 = c1.columns(2)
    
    with c3:
        GA_reset_button = st.button(label="Rénitialiser", key="GA_reset_button")
    
    with c4:
        GA_random_button = st.button(label="ajuster aléatoirement", key="GA_random_button")

    def change_settings(reset_iteration=1, option=0):
        
        GA_slider_place_holder1.empty()
        GA_slider_place_holder2.empty()
        GA_slider_place_holder3.empty()
        GA_slider_place_holder4.empty()
        
        if option == 1: # Rénitialiser paramètres
            values = values_list

        else: # option = 2 : ajuster les paramètres aléatoirement
            values = [choice(range(1, max_values_list[0])),
                    choice(range(1, int(max_values_list[1]*100)+1)) / 100,
                    choice(range(1, int(max_values_list[2]*100)+1)) / 100,
                    choice(range(1, max_values_list[3]))
                ]

        s1 = GA_slider_place_holder1.slider(label="Taille de la population initiale", 
                                            min_value=1, 
                                            max_value=max_values_list[0], 
                                            value=values[0], 
                                            key=GA_key1+reset_iteration)

        s2 = GA_slider_place_holder2.slider(label="Taux de mutation", 
                                            min_value=0.01, 
                                            max_value=max_values_list[1], 
                                            value=values[1], 
                                            step=0.01,  
                                            key=GA_key2+reset_iteration)

        s3 = GA_slider_place_holder3.slider(label="Taux de croisement", 
                                            min_value=0.01, 
                                            max_value=max_values_list[2], 
                                            value=values[2], 
                                            step=0.01,  
                                            key=GA_key3+reset_iteration)

        s4 = GA_slider_place_holder4.slider(label="Nombre de générations", 
                                            min_value=1, 
                                            max_value=max_values_list[3], 
                                            value=values[3], 
                                            key=GA_key4+reset_iteration)
        return s1, s2, s3, s4

    if GA_reset_button:
        GA_reset_button += 1
        GA_s1, GA_s2, GA_s3, GA_s4 = change_settings(GA_reset_button, 1)

    if GA_random_button:
        GA_reset_button += 1
        GA_s1, GA_s2, GA_s3, GA_s4 = change_settings(GA_reset_button, 2)

    return [GA_s1, GA_s2, GA_s3, GA_s4]

# Affichage des paramètres de l'algorithme des colonies de fourmis
def display_ACO_settings(option):

    st.header("Paramètres de l'algorithme des colonies de fourmis")

    # slider's keys
    ACO_key1 = 70000
    ACO_key2 = 80000
    ACO_key3 = 90000
    ACO_key4 = 100000
    ACO_key5 = 110000

    c1, c2 = st.columns([7,3])

    # maximum clique values
    maximum_clique_values = [20, 100, 0.99, 0.99, 2000]
    maximum_clique_max_values = [100, 100, 0.99, 0.99, 10000]

    # all cliques values
    all_cliques_values = [10, 10, 0.1, 0.1, 2000]
    all_cliques_max_values = [100, 100, 0.99, 0.99, 10000]
    
    # values lists
    values_list = maximum_clique_values if option == 1 else all_cliques_values
    max_values_list = maximum_clique_max_values if option == 1 else all_cliques_max_values

    with c1:
        
        # Sliders components
        ACO_slider_place_holder1 = st.empty()
        ACO_slider_place_holder2 = st.empty()
        ACO_slider_place_holder3 = st.empty()
        ACO_slider_place_holder4 = st.empty()
        ACO_slider_place_holder5 = st.empty()
        
        # Sliders

        ACO_s1 = ACO_slider_place_holder1.slider(label="Nombre de fourmis", 
                                            min_value=1, 
                                            max_value=max_values_list[0], 
                                            value=values_list[0], 
                                            key=ACO_key1)

        ACO_s2 = ACO_slider_place_holder2.slider(label="Quantité de phéromone initiale",
                                            min_value=1, 
                                            max_value=max_values_list[1], 
                                            value=values_list[1], 
                                            key=ACO_key2)
        
        ACO_s3 = ACO_slider_place_holder3.slider(label="Taux d'évaporation",
                                            min_value=0.1,
                                            max_value=max_values_list[2],
                                            value=values_list[2], 
                                            step=0.01,
                                            key=ACO_key3)
        
        ACO_s4 = ACO_slider_place_holder4.slider(label="Récompense", 
                                            min_value=0.1, 
                                            max_value=max_values_list[3], 
                                            value=values_list[3], 
                                            step=0.01,
                                            key=ACO_key4)
        
        ACO_s5 = ACO_slider_place_holder5.slider(label="Nombre d'itération", 
                                                min_value=1, 
                                                max_value=max_values_list[4],
                                                value=values_list[4],
                                                key=ACO_key5)

    with c2:
        animate("Components/ACO_animation.json", 450, 300)
        
    c3, c4 = c1.columns(2)

    with c3:
        ACO_reset_button = st.button(label="Rénitialiser", key="ACO_reset_button")
    
    with c4:
        ACO_random_button = st.button(label="ajuster aléatoirement", key="ACO_random_button")

    def change_settings(reset_iteration=1, option=0):

        ACO_slider_place_holder1.empty()
        ACO_slider_place_holder2.empty()
        ACO_slider_place_holder3.empty()
        ACO_slider_place_holder4.empty()
        ACO_slider_place_holder5.empty()

        if option == 1: # Rénitialiser paramètres
            values = values_list

        else: # Ajuster les paramètres aléatoirement
            values = [  choice(range(1, max_values_list[0])),
                        choice(range(1, max_values_list[1])), 
                        choice(range(1, int(max_values_list[2]*100)+1)) / 100,
                        choice(range(1, int(max_values_list[3]*100)+1)) / 100,
                        choice(range(1, max_values_list[4]))
                    ]
        
        s1 = ACO_slider_place_holder1.slider(label="Nombre de fourmis",
                                            min_value=1, 
                                            max_value =max_values_list[0], 
                                            value=values[0], 
                                            key=ACO_key1+reset_iteration)
                
        s2 = ACO_slider_place_holder2.slider(label="Quantité de phéromone initiale", 
                                            min_value=1, 
                                            max_value=max_values_list[1], 
                                            value=values[1], 
                                            key=ACO_key2+reset_iteration)
        
        s3 = ACO_slider_place_holder3.slider(label="Taux d'évaporation",
                                            min_value=0.1,
                                            max_value=max_values_list[2],
                                            value=values[2], 
                                            step=0.01, 
                                            key=ACO_key3+reset_iteration)
        
        s4 = ACO_slider_place_holder4.slider(label="Récompense",
                                            min_value=0.1, 
                                            max_value=max_values_list[3], 
                                            value=values[3], 
                                            step=0.01, 
                                            key=ACO_key4+reset_iteration)
        
        s5 = ACO_slider_place_holder5.slider(label="Nombre d'itération",
                                            min_value=1, 
                                            max_value=max_values_list[4], 
                                            value=values[4],  
                                            key=ACO_key5+reset_iteration)
            
        return s1, s2, s3, s4, s5

    if ACO_reset_button:
        ACO_reset_button += 1
        ACO_s1, ACO_s2, ACO_s3, ACO_s4, ACO_s5 = change_settings(ACO_reset_button, 1)

    if ACO_random_button:
        ACO_reset_button += 1
        ACO_s1, ACO_s2, ACO_s3, ACO_s4, ACO_s5 = change_settings(ACO_random_button, 2)

    return [ACO_s1, ACO_s2, ACO_s3, ACO_s4, ACO_s5]

# Affichage des paramètres du graphe aléatoire
def display_random_graph_settings(random_graph_name):
    
    # slider's keys
    random_graph_key1 = 120000
    random_graph_key2 = 130000
    
    random_graph_place_holder1 = st.empty()
    random_graph_place_holder2 = st.empty()

    # slider du nombre de sommet
    vertice_number = random_graph_place_holder1.slider(
                        label="Choisir le nombre de sommet",
                        value=100,
                        min_value=2,
                        max_value=200,
                        key=random_graph_key1)

    # Forumule qui calcule le nombre maximal d'arrêtes pour un nombre de sommet donné
    max_edges_number = vertice_number * (vertice_number - 1) // 2
 
    # slider du nombre d'arrêtes
    edges_number = random_graph_place_holder2.slider(
                            label="Choisir le nombre d'arrête", 
                            value=max_edges_number//2,
                            min_value=1,
                            max_value=max_edges_number,
                            key=random_graph_key2)   
    
    c1, c2 = st.columns(2)
    
    with c1:
        random_graph_button = st.button(label="ajuster aléatoirement", key="random_graph_button")

    def change_settings(reset_iteration=1):

        random_graph_place_holder1.empty()
        random_graph_place_holder2.empty()

        value1 = choice(range(2, 201))
        max_edges_number = value1 * (value1 - 1) // 2
        value2 = choice(range(1, max_edges_number+1))

        s1 = random_graph_place_holder1.slider(
                            label="Choisir le nombre de sommet",
                            value=value1,
                            min_value=2,
                            max_value=200,
                            key=random_graph_key1+reset_iteration)

        s2 = random_graph_place_holder2.slider(
                            label="Choisir le nombre d'arrête", 
                            value=value2,
                            min_value=1,
                            max_value=max_edges_number,
                            key=random_graph_key2+reset_iteration)
        
        return s1, s2
    
    if random_graph_button:
        random_graph_button += 1
        vertice_number, edges_number = change_settings(random_graph_button)

    # Afficher les bouton de validation si tout est bon
    if random_graph_name and vertice_number and edges_number:
        confirm_button = c2.button("Télécharger le graphe")
    
        if confirm_button:
            return [vertice_number, edges_number]
    
    # Retourner None si quelques chose manque
    return None, None