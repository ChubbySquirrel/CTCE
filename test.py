import pynauty as pyn

A = pyn.Graph(number_of_vertices=3,directed=False,adjacency_dict={0:[1],1:[0],2:[]},vertex_coloring=[set([0,1]),set([2])])
B = pyn.Graph(number_of_vertices=3,directed=False,adjacency_dict={0:[2],1:[],2:[0]},vertex_coloring=[set([0,1]),set([2])])

C = pyn.Graph({0:[1],1:[0],2:[]})
D = pyn.Graph({0:[2],1:[],2:[0]})

print(pyn.isomorphic(C,D))
print(pyn.isomorphic(A,B))
