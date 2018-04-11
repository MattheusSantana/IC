import timeit
import sys
from graph import *
from makeGraph import *
from tcg import *
import copy

# 1 Step: Generates K-graph
k = int(input()) #Number of vertices
Kgraph = makeKGraph(k)
trees = makeTrees(Kgraph)


file = open('treeK6.txt', 'r')
array = []
print("lendo arquivo...")
for line in file.readlines():
	a = list(map(int, line.split(',')))
	array.append(a)
print("arquivo lido!")	

results = []
count = 0
count1 = 0
graph = makeGraph("a")
graph.initializeColorTable()

for t in trees.treesList:
	t.dfs()
inicio = timeit.default_timer()
for i in array:
	count1+=1
	for t in trees.treesList:
		aux = deepcopy(t)
		aux.dfs()
		print(countOcurrences(graph, t))		
		
	print("*****************")
	upColor(trees.colors, i)
	if count1 == 10:
		break	
		#TCG(graph,t)
fim = timeit.default_timer()
print("%0.9f" %(fim - inicio))
'''print("*********************************")
for i in results:
	print(i)'''


	

#Kgraph.printVertices()
#Kgraph.printEdges()
#for e in Kgraph.edges:
#	print(e.u.id, e.v.id)
