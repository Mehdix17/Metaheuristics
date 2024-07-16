import ALGOS.SA_fonctions as SA
import ALGOS.GA_fonctions as GA
import ALGOS.ACO_fonctions as ACO

def maximum_clique(graph, p, timer, option):
    
    if option == 1:
        maximum_clique, calcul_time = SA.maximum_clique_finder(graph.graph_dic, 
                                                               p[0], p[1], p[2],
                                                               timer)
    elif option == 2:
        maximum_clique, calcul_time = GA.maximum_clique_finder(graph.graph_dic, 
                                                               p[0], p[1], p[2], p[3],
                                                               timer)
    else:
        maximum_clique, calcul_time = ACO.maximum_clique_finder(graph.graph_dic, 
                                                                p[0], p[1], p[2], p[3], p[4],
                                                                timer)
    return maximum_clique, calcul_time

def all_clique(graph, p, timer, option):

    if option == 1:
        all_clique_found, calcul_time = SA.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2],
                                                             timer)    
    elif option == 2:
        all_clique_found, calcul_time = GA.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2], p[3],
                                                             timer)
    else:
        all_clique_found, calcul_time = ACO.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2], p[3], p[4],
                                                             timer)   
    return all_clique_found, calcul_time

def vertex_maximum_clique(graph, vertex, p, timer, option):

    if option == 1:
        maximum_clique, calcul_time = SA.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                      vertex, 
                                                                      p[0], p[1], p[2],
                                                                      timer)
    
    elif option == 2:
        maximum_clique, calcul_time = GA.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                      vertex, 
                                                                      p[0], p[1], p[2], p[3],
                                                                      timer)
    
    else:
        maximum_clique, calcul_time = ACO.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                       vertex, 
                                                                       p[0], p[1], p[2], p[3], p[4],
                                                                       timer)
    return maximum_clique, calcul_time
