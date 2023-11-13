import pynauty as pyn

A = pyn.Graph(number_of_vertices=3,directed=False,adjacency_dict={0:[1],1:[0],2:[]},vertex_coloring=[set([0,1,2])])
B = pyn.Graph(number_of_vertices=3,directed=False,adjacency_dict={0:[2],1:[],2:[0]},vertex_coloring=[set([0,1,2])])
C = pyn.Graph(number_of_vertices=3,directed=False,adjacency_dict={0:[2,1],1:[0],2:[0]},vertex_coloring=[set([0,1,2])])
D = pyn.Graph(number_of_vertices=4,directed=False,adjacency_dict={0:[2,1],1:[3,0],2:[0],3:[1]},vertex_coloring=[set([0,1,2,3])])

E = pyn.Graph(number_of_vertices=4,directed=False,adjacency_dict={0:[1],1:[0],2:[3,0],3:[2,1]},vertex_coloring=[set([0,1,2,3])])
F = pyn.Graph(number_of_vertices=4,directed=False,adjacency_dict={0:[1],1:[2,0],2:[1,3],3:[2]},vertex_coloring=[set([0,1,2,3])])
list = [A,B,C,D,E,F]

def custom_equiv_set(lst, equivalence_relation):
    
    seen = []
    counting_list = []

    for i,item in enumerate(lst):
        seen_counter = 0
        if i == 0: 
            counting_list.append([item,1])
            seen.append(item)
            continue
        
        equivalent_found = False

        for j,seen_item in enumerate(seen):
            if equivalence_relation(item, seen_item)==True:
                equivalent_found = True
                a=j
                seen_counter+=1
                break
        
        if not equivalent_found:
            seen.append(item)
            counting_list.append([item,1])
            
        counting_list[a][1] += seen_counter


    return seen, counting_list

# Example usage:
# Define your custom equivalence relation function, for example:
def custom_equiv(a, b):
    # Your equivalence logic here
    return pyn.isomorphic(a,b)   # Example: consider two numbers equivalent if they have the same parity

# Test the algorithm
input_list = [A,B,C,D,E,F]
result_set, element_counter = custom_equiv_set(input_list, custom_equiv)
# print("Result Set:", result_set)
print("Element Counter:", element_counter)



