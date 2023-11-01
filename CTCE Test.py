import sympy as smp 
import numpy as np
import sys
import pynauty as pyn



F = smp.IndexedBase('F')
i,j = smp.symbols('i j', cls=smp.Idx)
C = smp.symbols('C')

#Expands the Meyer expansion symbollically and converts from sympy objects to list

#N is the given order N of interest, Order_C is 

def expand(N,Order_C): 
    
         
    expression = 0
    A = []
    Collected_terms = []
    for i in range (1,N+1):
        for j in range (i+1,N+1):
            A.append((1+C*F[i,j])) #Append each Meyer expansion term symbollically to list
            
    expr = smp.expand(smp.prod(A)-1) #multiply each term and subtract unity
    collected = smp.collect(expr,C) #Collect the expansion in orders of C

    print("collected == ", collected)

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


#Takes termlist and converts to a dictionary with keys for each order of C with order 1 at the 0 index. 
def IsConnected (termlist,N):
    elementdict = dict.fromkeys(range(0,N)) #Dictionary of graphs with key of the order of C
    for i, term in enumerate(termlist):
        B = [] #toy list
        if i == len(termlist)-1:
            new_tuple = tuple()
            for i, element in enumerate(term.args):
                new_tuple += element.indices
            B.append(new_tuple) #add it to list 
        else:
            for argi in term.args:
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
                        if i >= 1: 
                            intersection = itemset.intersect(subset) #calculate intersection 
                            if len(intersection) > 0:
                                new_tuple += tuple(argi2.indices) #save the connected indices
                                subset.union(intersection) #make the set include the new index
                    B.append(new_tuple) #add it list 

        elementdict[i] = B #then add to dict
                        
                        

    return elementdict # Rtur



# Calculate Isomorphism of all graphs in dict and keep tally of how many of each graph show up in a list
def isomorphism(dictionary,N):
    graph_dict = {} #New form of graphs as a list of tuples with first element being the adjacency list of graph
                    # and second being the number of times that graph shows up
    for key,value in dictionary.items(): 
        graph_dict[key] = []
        for graph in value:
            Adjacency_list = {key:[] for key in range(0,N)}#make dict of empty lists
            for i in range(len(graph)): #appending each tuple F index to an adjacency list
                if i%2 ==0:
                    Adjacency_list[graph[i]-1].append(graph[i+1]-1)
                if i%2 ==1:
                    Adjacency_list[graph[i]-1].append(graph[i-1]-1)
            graph_dict[key].append((Adjacency_list,1))
    
    for key,value in graph_dict.items():
        for i in range(0,len(value)):
            for j in range(i+1,len(value)):
                print(value[i][0],value[j][0])
                Graph1 = pyn.Graph(number_of_vertices=N,directed=False,adjacency_dict=value[i][0],vertex_coloring=[])
                Graph2 = pyn.Graph(number_of_vertices=N,directed=False,adjacency_dict=value[j][0],vertex_coloring=[])
                if pyn.isomorphic(Graph1,Graph2) == True:
                    value.remove(value[j])
                    value[i][1] += 1
            else:
                continue
            
    return graph_dict


def main(N,Order_C):
    Collected = expand(N,Order_C)
    print("expansion == ", Collected)
    Full_list = IsConnected(Collected,N)
    print("Connected Terms == ", Full_list)
    unique_list = isomorphism(Full_list,N)
    print("Unique List == ", unique_list)
    return

if __name__ == "__main__":
    main(3,0)


