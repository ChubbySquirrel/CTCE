import sympy as smp 
import numpy as np
import sys
import pynauty as pyn
import networkx as nx



F = smp.IndexedBase('F')
i,j = smp.symbols('i j', cls=smp.Idx)
C = smp.symbols('C')

#Expands the Meyer expansion symbollically and converts from sympy objects to list

#N is the given order N of interest, Order_C is 

def expand(N,Order_C): 
    
         
    """
    Expands the Meyer expansion symbolically and converts from sympy objects to a list.

    Parameters:
    - N: int, the given order N of interest
    - Order_C: int, the order of C

    Returns:
    - list: List of terms in the expansion
    """
         
    expression = 0
    A = []
    Collected_terms = []
    for i in range (1,N+1):
        for j in range (i+1,N+1):
            A.append((1+C*F[i,j])) #Append each Meyer expansion term symbollically to list
            
    expr = smp.expand(smp.prod(A)-1) #multiply each term and subtract unity
    collected = smp.collect(expr,C) #Collect the expansion in orders of C

    # print("collected == ", collected)

    global N1
    N1 = smp.binomial(N,2)
    
    for i in range(N1,0,-1): #This is just a weird quirk of how Sympy add objects are stored. 
        #Each addition term is an argument for an object with the "Add". 
        #This code converts from an add object to a list to make it easier to work with.
        Collected_terms.append(smp.Add(*[argi/(C**(i)) for argi in collected.args if argi.has(C**(i))]))
        collected = smp.Add(collected,*(-1*argi for argi in collected.args if argi.has(C**(i))))
    for i in range(1,N+1):
        for j in range(i+1,N+1): 
            expression += F[i,j] # The loop above works perfectly for all order other than 1 so this hardcodes O = 1
  

    Collected_terms.reverse()
        
    Collected_terms[0] = expression #Hard code order 1 because code above is weird for some reason
        
    if type(Order_C) == int:
        if Order_C == 0:
            return Collected_terms
        if Order_C != 0:
            return [Collected_terms[Order_C+1]]
    else:
        print('Order_C must be an Integer')


def IsConnected_old (termlist,N):
    
    
    if N ==2: 
        B = []
        for i, term in enumerate(termlist):
            B.append(term.indices)
        elementdict = {0:[B]}
    else:
        elementdict = dict.fromkeys(range(0,N1)) #Dictionary of graphs with key of the order of C
        for i, term in enumerate(termlist):
            B = [] #toy list to be appended later

            if i == len(termlist)-1:
                new_tuple = tuple()
                for i, element in enumerate(term.args):
                    new_tuple += element.indices
                B.append(new_tuple) #add it to list 
            else:
                for argi in term.args:
                    is_connected = True
                    if type(argi) == smp.tensor.indexed.Indexed: #if term is a solo term (Order C = 1)
                        B.append(tuple(smp.sets.sets.FiniteSet(*list(argi.indices))) )
                    if type(argi) == smp.core.mul.Mul: #if term is a multiplication of terms (Order C != 1)
                        new_list = argi.args
                        itemset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                        new_tuple = tuple()
                        subset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                        for i, argi2 in enumerate(new_list): #parse through each F in the multiplication
                            
                            if i== 0: #initialize set for first term
                                new_tuple += tuple(argi2.indices)
                            if i >= 1 and is_connected == True: 
                                itemset = smp.sets.sets.FiniteSet(*list(argi2.indices))
                                intersection = itemset.intersect(subset) #calculate intersection 
                                if len(intersection) > 0:
                                    new_tuple += tuple(argi2.indices) #save the connected indices
                                    subset.union(intersection) #make the set include the new index
                                if len(intersection) == 0:
                                    is_connected = False
                                    break
                                
                        if is_connected == True:
                            B.append(new_tuple) #add it list 
                        else:
                            continue

            if is_connected == True:
                elementdict[i] = B #then add to dict
            else:
                continue
                        
                        

    return elementdict # Rtur

def Makegraph(edgelist):
    G = nx.Graph()
    for i in range(len(edgelist)):
        G.add_edge(edgelist[i][0],edgelist[i][1])
    return G

def IsConnected (termlist,N):
    
    
    if N ==2: 
        B = []
        for i, term in enumerate(termlist):
            B.append(term.indices)
        elementdict = {0:[B]}
    else:
        elementdict ={new_list:[] for new_list in range(0,N1)} #Dictionary of graphs with key of the order of C
        for i, term in enumerate(termlist):
            B = [] #toy list to be appended later

            if i == len(termlist)-1:
                new_tuple = tuple()
                for j, element in enumerate(term.args):
                    new_tuple += element.indices
                elementdict[i].append([new_tuple]) #add it to list 
            else:
                for argi in term.args:
                    B = []

                    if type(argi) == smp.tensor.indexed.Indexed: #if term is a solo term (Order C = 1)

                        B.append(argi.indices)
                    if type(argi) == smp.core.mul.Mul: #if term is a multiplication of terms (Order C != 1)
                        new_list = argi.args

                        for k, argi2 in enumerate(new_list): #parse through each F in the multiplication

                            B.append(argi2.indices)
                                

                    Graph = Makegraph(B)
                    if nx.is_connected(Graph) == True:
                        elementdict[i].append(B)
                                
                            
    return elementdict # Rtur

def custom_equiv_set(lst, equivalence_relation):
    
    """
    Finds unique elements in a list based on a custom equivalence relation.

    Parameters:
    - lst: list, input list
    - equivalence_relation: function, custom equivalence relation

    Returns:
    - list: List of unique elements
    - list: List of counts for each unique element
    """
    
    counting_list = []
    a=0
    result = []
    for i,item in enumerate(lst):
        
        if i == 0: 
            counting_list.append([item,1])
            result.append(item)
            continue
        
        equivalent_found = False

        for j,seen_item in enumerate(result):
            if equivalence_relation(item, seen_item)==True:
                equivalent_found = True
                # a=j
                # seen_counter+=1
                counting_list[j][1] += 1
                break
        
        if not equivalent_found:
            result.append(item)
            counting_list.append([item,1])
            
        # counting_list[a][1] += seen_counter

    return result, counting_list


def MakeAdjlist(Graph,N):
    
    """
    Makes an adjacency list from a list of tuples.

    Parameters:
    - graph: list, list of tuples representing edges
    - N: int, the number of vertices

    Returns:
    - dict: Adjacency list
    """
    
    Adjacency_list = {key:[] for key in range(0,N)}#make dict of empty lists
    for edge in Graph:
        Adjacency_list[edge[0]-1].append(edge[1]-1)
        Adjacency_list[edge[1]-1].append(edge[0]-1)
    return Adjacency_list


def isomorphism(dictionary,N):
    
    """
    Calculates isomorphism of all graphs in the dictionary and keeps tally of each graph's occurrences.

    Parameters:
    - dictionary: dict, dictionary of graphs with keys as the order of C
    - N: int, the number of vertices

    Returns:
    - dict: Dictionary of isomorphic graphs for each order of C
    - dict: Condensed dictionary with the tally of each graph
    """
    
    graph_dict = {} #New form of graphs as a dictionary of list of graph objects for each order of C
    if  N ==2:
        iso_dict = {0:[[pyn.Graph(number_of_vertices=2,directed=False,adjacency_dict= {0:[1],1:[0]},vertex_coloring=[set([0,1])])],1]}
        condensed_dict = {0:[1]}
    
    else:
        for key,value in dictionary.items(): 
            graph_dict[key] = []
            for graph in value:
              
                Adj_list = MakeAdjlist(graph,N)
                #turn this adjacency list into graph objects
                new_graph = pyn.Graph(number_of_vertices=N,adjacency_dict=Adj_list,directed=False,vertex_coloring=[set(range(0,N))])
                graph_dict[key].append(new_graph)
    
    #new dictionary of isomorphic graphs for each order of C
        iso_dict ={} 
        condensed_dict = dict.fromkeys(range(1,N1+1))
        for key,value in graph_dict.items():
            new_value2 = []
            if len(value) > 1:
                new_value = custom_equiv_set(value,pyn.isomorphic)[1]
                iso_dict[key] = new_value
                for item in new_value:
                    new_value2.append(item[1])
                condensed_dict[key+1] = new_value2
                
            if len(value) == 1:
                new_value = [value,1]
                iso_dict[key] = new_value
                condensed_dict[key+1] = [1]
            
            
    return iso_dict ,condensed_dict


def main(N,Order_C,print_bool):
    
    """
    Main function to execute the entire process.

    Parameters:
    - N: int, the given order N of interest
    - Order_C: int, the order of C
    - print_bool: bool, whether to print intermediate results or not

    Returns:
    None
    """
    
    Collected = expand(N,Order_C)
    Full_list = IsConnected(Collected,N)
    unique_list = isomorphism(Full_list,N)[0]
    condensed_dict = isomorphism(Full_list,N)[1]
    
    
    
    if print_bool == True:
        print("Connected Terms == ", Full_list)
        # print("expansion == ", Collected)
        print("Unique List == ", unique_list)
    
    print("Condensed List == ", condensed_dict)
    
    return

if __name__ == "__main__":
    main(4,0,True)


