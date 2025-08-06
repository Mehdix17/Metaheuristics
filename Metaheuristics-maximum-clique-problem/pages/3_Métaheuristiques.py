import streamlit as st

st.write("# Description des Métaheuristiques")

st.write("## Recuit Simulé ")
c1, c2 = st.columns([7,3])

with c1:
    st.markdown("""
    Le recuit simulé est un algorithme d'optimisation inspiré du processus de recuit en métallurgie, où un matériau est chauffé puis refroidi lentement pour atteindre un état de faible énergie. L'algorithme explore l'espace de solutions en acceptant des solutions voisines avec une probabilité qui diminue au fil du temps, même si elles sont moins bonnes que la solution actuelle, ce qui permet d'éviter les minima locaux. Cette probabilité est contrôlée par un paramètre appelé température, qui décroît progressivement selon un schéma de refroidissement prédéfini. Le recuit simulé est particulièrement efficace pour résoudre des problèmes d'optimisation combinatoire tels que le voyageur de commerce (TSP) et la détermination de cliques maximales dans le graphes.
    """)

c2.image("Components\Images\SA_image.jpg", caption="Illustration du principe de recuit")

st.write("## L'algorithme génétique")
st.markdown("""L'algorithme génétique est une méthode d'optimisation inspirée des principes de la sélection naturelle et de la génétique. Il maintient une population de solutions potentielles, appelées individus, qui évoluent au fil des générations. Chaque individu est évalué selon une fonction de fitness, et les meilleurs individus sont sélectionnés pour se reproduire par croisement et mutation, créant ainsi une nouvelle génération de solutions. Les opérateurs de croisement et de mutation introduisent de la diversité dans la population, permettant à l'algorithme de découvrir de nouvelles solutions. L'algorithme génétique est largement utilisé pour des problèmes complexes comme la planification, l'ordonnancement et la recherche de cliques maximales dans les graphes.    """)

c1, c2 = st.columns([7,3])

with c1:
    st.image("Components\Images\GA_image1.jpg", caption="Illustration du concept de croisement")
    st.image("Components\Images\GA_image2.png", caption="Illustration de croisement en deux points")

with c2:
    st.image("Components\Images\GA_image3.png", caption="Organigramme de l'algorithme génétique")

st.write("## L'algorithme des colonies de fourmis")
st.markdown("""L'algorithme de colonie de fourmis s'inspire du comportement collectif des colonies de fourmis dans la nature, où les fourmis trouvent des chemins optimaux entre leur nid et une source de nourriture en déposant des phéromones sur les routes qu'elles empruntent. Cet algorithme modélise les solutions potentielles comme des chemins, et les fourmis artificielles explorent l'espace de solutions en suivant et en renforçant les chemins les plus prometteurs. La quantité de phéromone déposée et son évaporation au fil du temps permettent de balancer l'exploitation et l'exploration, aidant ainsi à éviter les minima locaux et à converger vers une solution optimale. L'algorithme de colonie de fourmis est efficace pour les problèmes de graphe tels que le problème du voyageur de commerce et la recherche de cliques maximales.""")

c1, c2, c3 = st.columns([2,6,2])
c2.image("Components\Images\ACO_image1.png", caption="Illustration du comportement des fourmis lors de la recherche de nourriture")
