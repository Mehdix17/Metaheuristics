import streamlit as st

st.title("Description des Benchmarks")

st.markdown("""
            
On peut classifier les graphes DIMACS en 3 types :
\n###### • Graphes de Compétition (Benchmark Graphs) 
\n###### • Graphes Aléatoires (Random Graphs)
\n###### • Graphes Structurés 

## 1) Graphes de Compétition (Benchmark Graphs) 
Ces graphes sont générés pour les compétitions DIMACS, ils ont été conçus pour tester les algorithmes de clique maximale, cette classe comporte 8 familles

## brock
Les instances de cette famille ont été conçus pour être difficiles et variés afin de fournier des Benchmarks rigoureux, à titre d’exemple le brock200_2 est un graphe avec 200 sommets et une certaine structure interne utilisée pour tester les algorithmes de clique maximale. 

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    | brock200_1    |   200   |   14834 |        21        |
    +---------------+---------+---------+------------------+
    | brock200_2    |   200   |    9876 |        12        |
    +---------------+---------+---------+------------------+
    | brock200_3    |   200   |   12048 |        15        |
    +---------------+---------+---------+------------------+
    | brock200_4    |   200   |   13089 |        17        |
    +---------------+---------+---------+------------------+
    | brock400_1    |   400   |   59723 |        27        |
    +---------------+---------+---------+------------------+
    | brock400_2    |   400   |   59786 |        29        |
    +---------------+---------+---------+------------------+
    | brock400_3    |   400   |   59681 |        31        |
    +---------------+---------+---------+------------------+
    | brock400_4    |   400   |   59765 |        33        |
    +---------------+---------+---------+------------------+
    | brock800_1    |   800   |  207505 |        23        |
    +---------------+---------+---------+------------------+
    | brock800_2    |   800   |  208166 |        24        |
    +---------------+---------+---------+------------------+
    | brock800_3    |   800   |  207333 |        25        |
    +---------------+---------+---------+------------------+
    | brock800_4    |   800   |  207643 |        26        |
    +---------------+---------+---------+------------------+

## c-fat
Ces graphes ont une structure de cluster claire. Par exemple, c-fat200-1 est un graphe avec 200 sommets organisé en clusters, la structure de cluster peut rendre la recherche de la clique maximale plus complexe.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    | c-fat200-1    |   200   |    1534 |        12        |
    +---------------+---------+---------+------------------+
    | c-fat200-2    |   200   |    3235 |        24        |
    +---------------+---------+---------+------------------+
    | c-fat200-5    |   200   |    8473 |        58        |
    +---------------+---------+---------+------------------+
    | c-fat500-1    |   500   |    4459 |        14        |
    +---------------+---------+---------+------------------+
    | c-fat500-2    |   500   |    9139 |        26        |
    +---------------+---------+---------+------------------+
    | c-fat500-5    |   500   |   23191 |        64        |
    +---------------+---------+---------+------------------+
            
## gen
Ces instances ont été créés pour tester une variété de problèmes combinatoires, notamment la clique maximale, la couverture de sommets et la coloration des graphes, Par exemple, gen200-p0.9-55 représente un graphe généré avec une probabilité de 0.9 pour chaque arête et d'autres paramètres spécifiques

    +----------------+---------+---------+------------------+
    | Nom du graphe  | Sommets |  Arêtes | Clique maximale  |
    +----------------+---------+---------+------------------+
    | gen200_p0.9_44 |   200   |  17910  |        44        |
    +----------------+---------+---------+------------------+
    | gen200_p0.9_55 |   200   |  17910  |        55        |
    +----------------+---------+---------+------------------+
    | gen400_p0.9_55 |   400   |  71820  |        55        |
    +----------------+---------+---------+------------------+
    | gen400_p0.9_65 |   400   |  71820  |        65        |
    +----------------+---------+---------+------------------+
    | gen400_p0.9_75 |   400   |  71820  |        75        |
    +----------------+---------+---------+------------------+
            
## keller
Les graphes keller sont utilisés pour des problèmes de pavage en théorie des graphes et pour les tests d'algorithmes de clique maximale. Ils sont basés sur le problème de Keller, un problème classique en géométrie discrète.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |    keller4    |   171   |    9435 |        11        |
    +---------------+---------+---------+------------------+
    |    keller5    |   776   |  225990 |        27        |
    +---------------+---------+---------+------------------+
    |    keller6    |   3361  | 4619898 |        59        |
    +---------------+---------+---------+------------------+
            
## MAN (Manhattan Grid Graphs)
Les graphes de la famille MAN sont des graphes de grille représentant une grille Manhattan. Ces graphes sont utilisés pour des tests d'algorithmes dans des environnements structurés en grille, comme les réseaux de villes ou les problèmes de routage. Ces instances sont tests dans des domaines tels que les réseaux de transport, les problèmes de routage et les algorithmes de recherche de chemin.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |   MANN_a9     |    45   |   918   |        16        |
    +---------------+---------+---------+------------------+
    |   MANN_a27    |   378   |  70551  |       126        |
    +---------------+---------+---------+------------------+
    |   MANN_a45    |   1035  |  533115 |       345        |
    +---------------+---------+---------+------------------+
    |   MANN_a81    |   3321  | 5506380 |      1100        |
    +---------------+---------+---------+------------------+
            
## p_hat (Partitioned Hat Graphs)
Les instances p_hat sont des graphes générés de manière aléatoire avec une structure de partition spécifique. Ils sont souvent utilisés pour tester la performance des algorithmes de clique maximale et d'autres problèmes combinatoires en raison de leur structure partitionnée.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |  p_hat300-1   |   300   |   10933 |         8        |
    +---------------+---------+---------+------------------+
    |  p_hat300-2   |   300   |   21928 |        25        |
    +---------------+---------+---------+------------------+
    |  p_hat300-3   |   300   |   33390 |        36        |
    +---------------+---------+---------+------------------+
    |  p_hat500-1   |   500   |   31569 |         9        |
    +---------------+---------+---------+------------------+
    |  p_hat500-2   |   500   |   62946 |        36        |
    +---------------+---------+---------+------------------+
    |  p_hat500-3   |   500   |   93800 |        49        |
    +---------------+---------+---------+------------------+
    |  p_hat700-1   |   700   |   60999 |        11        |
    +---------------+---------+---------+------------------+
    |  p_hat700-2   |   700   |  121728 |        44        |
    +---------------+---------+---------+------------------+
    |  p_hat700-3   |   700   |  183010 |        62        |
    +---------------+---------+---------+------------------+
    |  p_hat1000-1  |   1000  |  122253 |        10        |
    +---------------+---------+---------+------------------+
    |  p_hat1000-2  |   1000  |  244799 |        46        |
    +---------------+---------+---------+------------------+
    |  p_hat1000-3  |   1000  |  371746 |        65        |
    +---------------+---------+---------+------------------+
    |  p_hat1500-1  |   1500  |  284923 |        12        |
    +---------------+---------+---------+------------------+
    |  p_hat1500-2  |   1500  |  568960 |        65        |
    +---------------+---------+---------+------------------+
    |  p_hat1500-3  |   1500  |  847244 |        94        |
    +---------------+---------+---------+------------------+
               
## san (Structured Network Graphs)
Les graphes de la famille san sont des graphes structurés générés avec des densités variées et une structure interne spécifique. Conçus pour tester les algorithmes de clique maximale et pour évaluer la performance des algorithmes sur des graphes denses et structurés.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    | san200_0.7_1  |   200   |   13930 |        30        |
    +---------------+---------+---------+------------------+
    | san200_0.7_2  |   200   |   13930 |        18        |
    +---------------+---------+---------+------------------+
    | san200_0.9_1  |   200   |   17910 |        70        |
    +---------------+---------+---------+------------------+
    | san200_0.9_2  |   200   |   17910 |        60        |
    +---------------+---------+---------+------------------+
    | san200_0.9_3  |   200   |   17910 |        44        |
    +---------------+---------+---------+------------------+
    | san400_0.5_1  |   400   |   39900 |        13        |
    +---------------+---------+---------+------------------+
    | san400_0.7_1  |   400   |   55860 |        40        |
    +---------------+---------+---------+------------------+
    | san400_0.7_2  |   400   |   55860 |        30        |
    +---------------+---------+---------+------------------+
    | san400_0.7_3  |   400   |   55860 |        22        |
    +---------------+---------+---------+------------------+
    | san400_0.9_1  |   400   |   71820 |       100        |
    +---------------+---------+---------+------------------+
    |    san1000    |   1000  |  250500 |        15        |
    +---------------+---------+---------+------------------+
            
## sanr (Randomized Structured Network Graphs)
Les sanr sont des variantes des graphes san avec une composante aléatoire ajoutée à leur génération. Ces graphes sont conçus pour introduire une variation supplémentaire dans les tests des algorithmes de clique maximale.
Utilisés pour tester les algorithmes de clique maximale avec une variation supplémentaire, ce qui permet de vérifier la robustesse des algorithmes face à des structures légèrement différentes.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |  sanr200_0.7  |   200   |  13868  |        18        |
    +---------------+---------+---------+------------------+
    |  sanr200_0.9  |   200   |  17863  |        42        |
    +---------------+---------+---------+------------------+
    |  sanr400_0.5  |   400   |  39984  |        13        |
    +---------------+---------+---------+------------------+
    |  sanr400_0.7  |   400   |  55869  |        21        |
    +---------------+---------+---------+------------------+
            
\n## 2) Graphes Aléatoires
Cette classe contient 2 familles : C et DSJC, ces graphes aléatoires sont conçus pour évaluer la capacité des algorithmes à colorier les graphes avec un nombre minimum de couleurs sans que deux sommets adjacents partagent la même couleur

## C (Random Coloring Graphs)
Incluent des instances comme C125.9, où 125 représente le nombre de sommets et 0.9 la probabilité qu'une arête existe entre deux sommets donnés. 

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |    C125.9     |   125   |   6963  |        34        |
    +---------------+---------+---------+------------------+
    |    C250.9     |   250   |  27984  |        44        |
    +---------------+---------+---------+------------------+
    |    C500.9     |   500   |  112332 |        57        |
    +---------------+---------+---------+------------------+
    |    C1000.9    |   1000  |  450079 |        68        |
    +---------------+---------+---------+------------------+
    |    C2000.5    |   2000  |  999836 |        16        |
    +---------------+---------+---------+------------------+
    |    C2000.9    |   2000  | 1799532 |        80        |
    +---------------+---------+---------+------------------+
    |    C4000.5    |   4000  | 4000268 |        18        |
    +---------------+---------+---------+------------------+
            

## DSJC (DIMACS-Structured Johnson Coloring Graphs)
Les instances de cette famille sont plus complexes et plus denses que les C, par exemple le DSJC500.5 a 500 sommets avec une probabilité de 0.5 pour l'existence d'une arête entre deux sommets. Ils servent de benchmarks plus difficiles pour évaluer la performance des algorithmes de coloration.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |   DSJC500_5   |   500   |  125248 |        13        |
    +---------------+---------+---------+------------------+
    |   DSJC1000_5  |   1000  |  499652 |        15        |
    +---------------+---------+---------+------------------+
            

\n## 3) Graphes Structurés
Les Graphes de cette classe sont des graphes générés avec une structure interne spécifique, souvent basés sur des concepts mathématiques ou combinatoires. 
Elle inclue 2 familles : hamming et johnson.

## hamming
Ces graphes sont basés sur les codes de Hamming. Par exemple, hamming6-2 représente un graphe où chaque sommet correspond à un mot de code de Hamming de longueur 6 et chaque arête existe si les mots de code sont à une distance de Hamming de 2.
Les graphes de Hamming sont souvent utilisés pour tester les algorithmes de couverture et domination de sommets et d'autres problèmes de graphes. Ils sont particulièrement pertinents pour les problèmes de codage et de théorie des codes, où les distances de Hamming jouent un rôle crucial.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    |  hamming6-2   |    64   |    1824 |        32        |
    +---------------+---------+---------+------------------+
    |  hamming6-4   |    64   |     704 |         4        |
    +---------------+---------+---------+------------------+
    |  hamming8-2   |   256   |   31616 |       128        |
    +---------------+---------+---------+------------------+
    |  hamming8-4   |   256   |   20864 |        16        |
    +---------------+---------+---------+------------------+
    |  hamming10-2  |   1024  |  518656 |       512        |
    +---------------+---------+---------+------------------+
    |  hamming10-4  |   1024  |  434176 |        40        |
    +---------------+---------+---------+------------------+
            
## johnson
Ces graphes sont basés sur les ensembles Johnson. Par exemple, johnson8-4-4 représente un graphe où les sommets sont des sous-ensembles de taille 4 d'un ensemble de 8 éléments, et il y a une arête entre deux sommets si les sous-ensembles correspondants ont exactement 4 éléments en commun.
Les graphes de Johnson sont utilisés pour tester les algorithmes de couverture de sommets et de clique maximale. Ils sont aussi employés dans des problèmes de combinatoire où les ensembles de k-éléments et leurs intersections jouent un rôle important.

    +---------------+---------+---------+------------------+
    | Nom du graphe | Sommets | Arêtes  | Clique maximale  |
    +---------------+---------+---------+------------------+
    | johnson8-2-4  |    28   |     210 |        4         |
    +---------------+---------+---------+------------------+
    | johnson8-4-4  |    70   |    1855 |        14        |
    +---------------+---------+---------+------------------+
    | johnson16-2-4 |   120   |    5460 |         8        |
    +---------------+---------+---------+------------------+
    | johnson32-2-4 |   496   |  107880 |        16        |
    +---------------+---------+---------+------------------+

""")