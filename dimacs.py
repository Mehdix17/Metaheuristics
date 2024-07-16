
# Classe des objets graphes
class Graph:
    def __init__(self, name, nodes, edges, clique_size, graph_dic, file_path):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.clique_size = clique_size
        self.graph_dic = graph_dic
        self.file_path = file_path

# Source : http://archive.dimacs.rutgers.edu/pub/challenge/graph/solvers/results.dmclique

# Source : https://iridia.ulb.ac.be/~fmascia/maximum_clique/DIMACS-benchmark

# Lien du Drive pour télécharger les 80 graphes :
# https://drive.google.com/file/d/1zzu9n5t97zKa_N_udLH-oAeMp1s02u6d/view?usp=drive_link 

# Création des 80 objets de type graphe

graphe1 = Graph(
            "brock200_1", 
            200,
            14834,
            21,
            {},
            r"DIMACS\brock200_1.clq"
            )

graphe2 = Graph(
            "brock200_2", 
            200,
            9876,
            12,
            {},
            r"DIMACS\brock200_2.clq"            
            )

graphe3 = Graph(
            "brock200_3", 
            200,
            12048,
            15,
            {},
            r"DIMACS\brock200_3.clq"            
            )

graphe4 = Graph(
            "brock200_4", 
            200,
            13089,
            17,
            {},
            r"DIMACS\brock200_4.clq"            
            )

graphe5 = Graph(
            "brock400_1", 
            400,
            59723,
            27,
            {},
            r"DIMACS\brock400_1.clq"            
            )

graphe6 = Graph(
            "brock400_2", 
            400,
            59786,
            29,
            {},
            r"DIMACS\brock400_2.clq"            
            )

graphe7 = Graph(
            "brock400_3", 
            400,
            59681,
            31,
            {},
            r"DIMACS\brock400_3.clq"            
            )

graphe8 = Graph(
            "brock400_4", 
            400,
            59765,
            33,
            {},
            r"DIMACS\brock400_4.clq"            
            )

graphe9 = Graph(
            "brock800_1", 
            800,
            207505,
            23,
            {},
            r"DIMACS\brock800_1.clq"            
            )

graphe10 = Graph(
            "brock800_2", 
            800,
            208166,
            24,
            {},
            r"DIMACS\brock800_2.clq"            
            )

graphe11 = Graph(
            "brock800_3", 
            800,
            207333,
            25,
            {},
            r"DIMACS\brock800_3.clq"            
            )

graphe12 = Graph(
            "brock800_4", 
            800,
            207643,
            26,
            {},
            r"DIMACS\brock800_4.clq"            
            )

graphe13 = Graph(
            "C125.9", 
            125,
            6963,
            34,
            {},
            r"DIMACS\C125.9.clq"
            )

graphe14 = Graph(
            "C250.9", 
            250,
            27984,
            44,
            {},
            r"DIMACS\C250.9.clq"
            )

graphe15 = Graph(
            "C500.9", 
            500,
            112332,
            57,
            {},
            r"DIMACS\C500.9.clq"
            )

graphe16 = Graph(
            "C1000.9", 
            1000,
            450079,
            68,
            {},
            r"DIMACS\C1000.9.clq"
            )

graphe17 = Graph(
            "C2000.5", 
            2000,
            999836,
            16,
            {},
            r"DIMACS\C2000.5.clq"
            )

graphe18 = Graph(
            "C2000.9", 
            2000,
            1799532,
            80,
            {},
            r"DIMACS\C2000.9.clq"
            )

graphe19 = Graph(
            "C4000.5", 
            4000,
            4000268,
            18,
            {},
            r"DIMACS\C4000.5.clq"
            )

graphe20 = Graph(
            "DSJC500_5", 
            500,
            125248,
            13,
            {},
            r"DIMACS\DSJC500_5.clq"            
            )

graphe21 = Graph(
            "DSJC1000_5", 
            1000,
            499652,
            15,
            {},
            r"DIMACS\DSJC1000_5.clq"            
            )

graphe22 = Graph(
            "keller4", 
            171,
            9435,
            11,
            {},
            r"DIMACS\keller4.clq"            
            )

graphe23 = Graph(
            "keller5", 
            776,
            225990,
            27,
            {},
            r"DIMACS\keller5.clq"            
            )

graphe24 = Graph(
            "keller6", 
            3361,
            4619898,
            59,
            {},
            r"DIMACS\keller6.clq"            
            )

graphe25 = Graph(
            "MANN_a9", 
            45,
            918,
            16,
            {},
            r"DIMACS\MANN_a9.clq"            
            )

graphe26 = Graph(
            "MANN_a27", 
            378,
            70551,            
            126,
            {},
            r"DIMACS\MANN_a27.clq"            
            )

graphe27 = Graph(
            "MANN_a45", 
            1035,
            533115,            
            345,
            {},
            r"DIMACS\MANN_a45.clq"            
            )

graphe28 = Graph(
            "MANN_a81", 
            3321,
            5506380,           
            1100,
            {},
            r"DIMACS\MANN_a81.clq"            
            )


graphe29 = Graph(
            "hamming6-2",
            64,
            1824, 
            32,
            {},
            r"DIMACS\hamming6-2.clq"
            )

graphe30 = Graph(
            "hamming6-4",
            64,
            704, 
            4,
            {},
            r"DIMACS\hamming6-4.clq"
            )

graphe31 = Graph(
            "hamming8-2",
            256,
            31616, 
            128,
            {},
            r"DIMACS\hamming8-2.clq"
            )

graphe32 = Graph(
            "hamming8-4",
            256,
            20864, 
            16,
            {},
            r"DIMACS\hamming8-4.clq"
            )

graphe33 = Graph(
            "hamming10-2",
            1024,
            518656, 
            512,
            {},
            r"DIMACS\hamming10-2.clq"
            )

graphe34 = Graph(
            "hamming10-4",
            1024,
            434176, 
            40,
            {},
            r"DIMACS\hamming10-4.clq"
            )

graphe35 = Graph(
            "gen200_p0.9_44",
            200,
            17910, 
            44,
            {},
            r"DIMACS\gen200_p0.9_44.clq"
            )

graphe36 = Graph(
            "gen200_p0.9_55",
            200,
            17910, 
            55,
            {},
            r"DIMACS\gen200_p0.9_55.clq"
            )

graphe37 = Graph(
            "gen400_p0.9_55",
            400,
            71820, 
            55,
            {},
            r"DIMACS\gen400_p0.9_55.clq"
            )

graphe38 = Graph(
            "gen400_p0.9_65",
            400,
            71820, 
            65,
            {},
            r"DIMACS\gen400_p0.9_65.clq"
            )

graphe39 = Graph(
            "gen400_p0.9_75",
            400,
            71820, 
            75,
            {},
            r"DIMACS\gen400_p0.9_75.clq"
            )

graphe40 = Graph(
            "c-fat200-1",
            200,
            1534, 
            12,
            {},
            r"DIMACS\c-fat200-1.clq"
            )

graphe41 = Graph(
            "c-fat200-2",
            200,
            3235, 
            24,
            {},
            r"DIMACS\c-fat200-2.clq"
            )

graphe42 = Graph(
            "c-fat200-5",
            200,
            8473, 
            58,
            {},
            r"DIMACS\c-fat200-5.clq"
            )

graphe43 = Graph(
            "c-fat500-1",
            500,
            4459, 
            14,
            {},
            r"DIMACS\c-fat500-1.clq"
            )

graphe44 = Graph(
            "c-fat500-2",
            500,
            9139, 
            26,
            {},
            r"DIMACS\c-fat500-2.clq"
            )

graphe45 = Graph(
            "c-fat500-5",
            500,
            23191, 
            64,
            {},
            r"DIMACS\c-fat500-5.clq"
            )

graphe46 = Graph(
            "c-fat500-10",
            500,
            46627, 
            126,
            {},
            r"DIMACS\c-fat500-10.clq"
            )

graphe47 = Graph(
            "johnson8-2-4",
            28,
            210, 
            4,
            {},
            r"DIMACS\johnson8-2-4.clq"
            )

graphe48 = Graph(
            "johnson8-4-4",
            70,
            1855, 
            14,
            {},
            r"DIMACS\johnson8-4-4.clq"
            )

graphe49 = Graph(
            "johnson16-2-4",
            120,
            5460, 
            8,
            {},
            r"DIMACS\johnson16-2-4.clq"
            )

graphe50 = Graph(
            "johnson32-2-4",
            496,
            107880, 
            16,
            {},
            r"DIMACS\johnson32-2-4.clq"
            )

graphe51 = Graph(
            "p_hat300-1",
            300,
            10933, 
            8,
            {},
            r"DIMACS\p_hat300-1.clq"
            )

graphe52 = Graph(
            "p_hat300-2",
            300,
            21928, 
            25,
            {},
            r"DIMACS\p_hat300-2.clq"
            )

graphe53 = Graph(
            "p_hat300-3",
            300,
            33390, 
            36,
            {},
            r"DIMACS\p_hat300-3.clq"
            )

graphe54 = Graph(
            "p_hat500-1",
            500,
            31569, 
            9,
            {},
            r"DIMACS\p_hat500-1.clq"
            )

graphe55 = Graph(
            "p_hat500-2",
            500,
            62946, 
            36,
            {},
            r"DIMACS\p_hat500-2.clq"
            )

graphe56 = Graph(
            "p_hat500-3",
            500,
            93800, 
            49,
            {},
            r"DIMACS\p_hat500-3.clq"
            )

graphe57 = Graph(
            "p_hat700-1",
            700,
            60999, 
            11,
            {},
            r"DIMACS\p_hat700-1.clq"
            )

graphe58 = Graph(
            "p_hat700-2",
            700,
            121728, 
            44,
            {},
            r"DIMACS\p_hat700-2.clq"
            )

graphe59 = Graph(
            "p_hat700-3",
            700,
            183010, 
            62,
            {},
            r"DIMACS\p_hat700-3.clq"
            )

graphe60 = Graph(
            "p_hat1000-1",
            1000,
            122253, 
            10,
            {},
            r"DIMACS\p_hat1000-1.clq"
            )

graphe61 = Graph(
            "p_hat1000-2",
            1000,
            244799, 
            46,
            {},
            r"DIMACS\p_hat1000-2.clq"
            )

graphe62 = Graph(
            "p_hat1000-3",
            1000,
            371746, 
            65,
            {},
            r"DIMACS\p_hat1000-3.clq"
            )

graphe63 = Graph(
            "p_hat1500-1",
            1500,
            284923, 
            12,
            {},
            r"DIMACS\p_hat1500-1.clq"
            )

graphe64 = Graph(
            "p_hat1500-2",
            1500,
            568960, 
            65,
            {},
            r"DIMACS\p_hat1500-2.clq"
            )

graphe65 = Graph(
            "p_hat1500-3",
            1500,
            847244, 
            94,
            {},
            r"DIMACS\p_hat1500-3.clq"
            )

graphe66 = Graph(
            "san200_0.7_1",
            200,
            13930, 
            30,
            {},
            r"DIMACS\san200_0.7_1.clq"
            )

graphe67 = Graph(
            "san200_0.7_2",
            200,
            13930, 
            18,
            {},
            r"DIMACS\san200_0.7_2.clq"
            )

graphe68 = Graph(
            "san200_0.9_1",
            200,
            17910, 
            70,
            {},
            r"DIMACS\san200_0.9_1.clq"
            )

graphe69 = Graph(
            "san200_0.9_2",
            200,
            17910, 
            60,
            {},
            r"DIMACS\san200_0.9_2.clq"
            )

graphe70 = Graph(
            "san200_0.9_3",
            200,
            17910, 
            44,
            {},
            r"DIMACS\san200_0.9_3.clq"
            )

graphe71 = Graph(
            "san400_0.5_1",
            400,
            39900, 
            13,
            {},
            r"DIMACS\san400_0.5_1.clq"
            )

graphe72 = Graph(
            "san400_0.7_1",
            400,
            55860, 
            40,
            {},
            r"DIMACS\san400_0.7_1.clq"
            )

graphe73 = Graph(
            "san400_0.7_2",
            400,
            55860, 
            30,
            {},
            r"DIMACS\san400_0.7_2.clq"
            )

graphe74 = Graph(
            "san400_0.7_3",
            400,
            55860, 
            22,
            {},
            r"DIMACS\san400_0.7_3.clq"
            )

graphe75 = Graph(
            "san400_0.9_1",
            400,
            71820, 
            100,
            {},
            r"DIMACS\san400_0.9_1.clq"
            )

graphe76 = Graph(
            "san1000",
            1000,
            250500, 
            15,
            {},
            r"DIMACS\san1000.clq"            
            )

graphe77 = Graph(
            "sanr200_0.7",
            200,
            13868, 
            18,
            {},
            r"DIMACS\sanr200_0.7.clq"
            )

graphe78 = Graph(
            "sanr200_0.9",
            200,
            17863, 
            42,
            {},
            r"DIMACS\sanr200_0.9.clq"
            )

graphe79 = Graph(
            "sanr400_0.5",
            400,
            39984, 
            13,
            {},
            r"DIMACS\sanr400_0.5.clq"
            )

graphe80 = Graph(
            "sanr400_0.7",
            400,
            55869, 
            21,
            {},
            r"DIMACS\sanr400_0.7.clq"
            )

# Liste des 80 graphes DIMACS
graph_list = [
    graphe1, graphe2, graphe3, graphe4, graphe5, graphe6, graphe7, graphe8, graphe9, graphe10,
    graphe11, graphe12, graphe13, graphe14, graphe15, graphe16, graphe17, graphe18, graphe19, graphe20,
    graphe21, graphe22, graphe23, graphe24, graphe25, graphe26, graphe27, graphe28, graphe29, graphe30,
    graphe31, graphe32, graphe33, graphe34, graphe35, graphe36, graphe37, graphe38, graphe39, graphe40,
    graphe41, graphe42, graphe43, graphe44, graphe45, graphe46, graphe47, graphe48, graphe49, graphe50,
    graphe51, graphe52, graphe53, graphe54, graphe55, graphe56, graphe57, graphe58, graphe59, graphe60,
    graphe61, graphe62, graphe63, graphe64, graphe65, graphe66, graphe67, graphe68, graphe69, graphe70,
    graphe71, graphe72, graphe73, graphe74, graphe75, graphe76, graphe77, graphe78, graphe79, graphe80
]

# Liste des noms des 80 graphes DIMACS
graph_names_list = [graph.name for graph in graph_list]
