import sympy as smp 
import numpy as np
import sys
import pynauty as pyn



F = smp.IndexedBase('F')
i,j = smp.symbols('i j', cls=smp.Idx)
C = smp.symbols('C')

def expand(N):
    expression = 0
    A = []
    Collected_terms = []
    for i in range (1,N+1):
        for j in range (i+1,N+1):
            A.append((1+C*F[i,j]))
            
    expr = smp.expand(smp.prod(A)-1)
    collected = smp.collect(expr,C)

    print(collected)


    # f = smp.polys.polytools.LT(collected)

    # # for i in range (N,0,-1):
    # #     Collected_terms.append()
    

    N1 = smp.binomial(N,2)
    for i in range(N1,0,-1):
        Collected_terms.append(smp.Add(*[argi/(C**(i)) for argi in collected.args if argi.has(C**(i))]))
        collected = smp.Add(collected,*(-1*argi for argi in collected.args if argi.has(C**(i))))
        #A crude way to do it, it would be much more efficent to start my removing the lower order terms but sympy weird
    Collected_terms.reverse()

    for i in range(1,N+1):
        for j in range(i+1,N+1): 
                expression += F[i,j]

 
    Collected_terms[0] = expression

    return Collected_terms


def IsConnected (termlist,N):
    elementdict = dict.fromkeys(range(1,N+1))
    
    for i, element in enumerate(termlist):
        B = []
        for argi in element.args:
            if type(argi) == smp.tensor.indexed.Indexed:
                B.append(tuple(smp.sets.sets.FiniteSet(*list(argi.indices))) )
            if type(argi) == smp.core.mul.Mul:
                new_list = argi.args
                itemset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                new_tuple = tuple()
                subset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                for i, argi2 in enumerate(new_list):
                    
                    if i== 0:
                        new_tuple += tuple(argi2.indices)
                    if i >= 1:
                        intersection = itemset.intersect(subset)
                        if len(intersection) > 0:
                            new_tuple += tuple(argi2.indices)
                            subset.union(intersection)
                B.append(new_tuple)

        elementdict[i+1] = B 
                        
                        

    return elementdict

def isconnected2 (termlist,N):
    adj_list = dict.fromkeys(range(0,N))

    for i, element in enumerate(termlist):
        B = []
        for argi in element.args:
            if type(argi) == smp.tensor.indexed.Indexed:
                B.append(tuple(smp.sets.sets.FiniteSet(*list(argi.indices))) )
            if type(argi) == smp.core.mul.Mul:
                new_list = argi.args
                itemset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                new_tuple = tuple()
                subset = smp.sets.sets.FiniteSet(*list(new_list[0].indices))
                for i, argi2 in enumerate(new_list):
                    
                    if i== 0:
                        new_tuple += tuple(argi2.indices)
                    if i >= 1:
                        intersection = itemset.intersect(subset)
                        if len(intersection) > 0:
                            new_tuple += tuple(argi2.indices)
                            subset.union(intersection)
                B.append(new_tuple)

        elementdict[i+1] = B 


    return adj_list


def Adjacency_list(dict,N):
    for key in dict:


    return adj_list


def main(N):
    Collected = expand(N)
    print("expansion == ", Collected)
    Full_list = IsConnected(Collected,N)
    print("Connected Terms == ", Full_list)
    return

if __name__ == "__main__":
    main(4)


