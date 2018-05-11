from graph import *
from sub import *
from copy import deepcopy


'''
	color0 = Color(0)
	color1 = Color(1)
	color2 = Color(2)
	color3 = Color(3)
	color4 = Color(4)
	color5 = Color(5)'''
def makeKGraph(k, labels):
	Kgraph = Graph()
	for i in range(k):
		vertex = Vertex()
		vertex.id = i
		vertex.label = labels[i]
		Kgraph.vList.append(vertex)

	for i in range(len(Kgraph.vList)):
		for j in range(i+1, len(Kgraph.vList),1):
			edge = Edge()
			edge.u = Kgraph.vList[i]			#Receive vertex object
			edge.v = Kgraph.vList[j]			#Receive vertex object
			Kgraph.eList.append(edge)
			Kgraph.vList[i].neighbors.append(Kgraph.vList[j])				
			Kgraph.vList[j].neighbors.append(Kgraph.vList[i])
			
	return Kgraph		

def makeGraphPPI(archive):
	file = open(archive, 'r')
	firstLine = file.readline() 
	verticesNumber, colorsNumber = firstLine.split(',')
	graph = Graph()
	graph.maxN = int(verticesNumber)
	graph.maxColor = int(colorsNumber)

	#Make Vertices.
	for i in range(graph.maxN):
		line = file.readline()
		v = Vertex()
		string1, label = string1, string2 = line.split()
		index, color = string1.split(':')
		v.id = int(index)
		v.color = int(color)
		v.label = label
		graph.vList.append(v)
	lines = file.readlines()
	
	#Make Edges.
	for line in lines:
		index, adj = map(int,line.split('-'))
		edge = Edge()
		edge.u = graph.vList[index]
		edge.v = graph.vList[adj]
		graph.vList[index].neighbors.append(graph.vList[adj])
		graph.vList[adj].neighbors.append(graph.vList[index])
		graph.eList.append(edge)


	return graph	



def makeGraph(entry):
		graph = Graph()	
		#Open archive reference to graph
		archive = open(entry, 'r')
		#archive =  open('graph-3.txt', 'r')
		#reading number of vertices and number maxime of colors
		firstLine = archive.readline()

		verticesNumber, colorsNumber = firstLine.split(',')
		graph.maxN = int(verticesNumber)
		graph.maxColor = int(colorsNumber)

		#Initializing vertices
		for i in range(graph.maxN):
			line = archive.readline()
			string1, string2 = line.split()
			index, color = string1.split(':')
			label, ec = string2.split(':')

			vertex = Vertex()
			vertex.id = int(index)
			vertex.color = int(color)
			vertex.label = label
			vertex.ecNumber = ec

			graph.vList.append(vertex)
			graph.n += 1

		#Adding neighbors of the vertices
		for line in archive.readlines():
			index, adj = line.split('-')
			
			graph.vList[int(index)].neighbors.append(graph.vList[int(adj)])
			graph.vList[int(adj)].neighbors.append(graph.vList[int(index)])


		archive.close()		
		return graph
			
#creates a graph referring to the input file		
def makeMotif(archive):
	motif = Graph()
	arc = open(archive, 'r')
	entry = arc.readline()
	numberVertices, maxColor = entry.split(',')
	motif.maxN = int(numberVertices)
	motif.maxColor = int(maxColor)

	for i in range(motif.maxN):
		line = arc.readline()
		index, color = line.split(':')
		vertex = Vertex()
		vertex.id = int(index)
		color = Color(int(color))
		vertex.color = color
		motif.vList.append(vertex)
		motif.n += 1
	
	lines = arc.readlines()
	
	for line in lines:
		index, neighbor = line.split('-')

		#Adding Edges between the vertices
		motif.vList[int(index)].neighbors.append(motif.vList[int(neighbor)])
		motif.vList[int(neighbor)].neighbors.append(motif.vList[int(index)])	
	arc.close()	
	return motif

def makeAllMotifsPPI(archive):
	trees = []
	#read file and make trees
	file = open(archive, 'r')
	verticesNumber = int(file.readline())
	#lines = file.readlines()
	labels = list(map(str, file.readlines()[1].split(" ")))
	
	if verticesNumber <=2:
		motif = Graph()
		for i in range(verticesNumber):
			v = Vertex()
			v.id=i
			v.color = i+1
			v.label= labels[i]
			motif.vList.append(v)	
		if verticesNumber == 2:
			motif.vList[0].neighbors.append(motif.vList[1])
			motif.vList[1].neighbors.append(motif.vList[0])
		trees.append(motif)
		
	
	else:
		Kgraph = makeKGraph(verticesNumber, labels)	
		trees = makeTreesPPI(Kgraph)
	return trees
	
#return a set of trees represented by edges list
def makeTreesPPI(Kgraph):
	array = []
	array = seq(len(Kgraph.eList), len(Kgraph.vList)-1)
	
	trees = []
	finalTrees = []
	counter = 0
	for i in array:
		graphAux = deepcopy(Kgraph)
		if kruskal(i, graphAux):
			trees.append(i)
			counter+=1 
	for i in trees:
		tree = Graph()
		for j in range(len(i)+1):
			vertex = Vertex()
			vertex.id = j
			vertex.color = j
			vertex.label = Kgraph.vList[j].label
			tree.vList.append(vertex)
		for e in i:
			tree.vList[Kgraph.eList[e].u.id].neighbors.append(tree.vList[Kgraph.eList[e].v.id])
			tree.vList[Kgraph.eList[e].v.id].neighbors.append(tree.vList[Kgraph.eList[e].u.id])
			tree.eList.append(Kgraph.eList[e])
		finalTrees.append(tree)	
	return finalTrees	
def makeTrees(Kgraph):
	array = []
	array = seq(len(Kgraph.eList), len(Kgraph.vList)-1)
	
	trees = []

	counter = 0
	for i in array:
		graphAux = deepcopy(Kgraph)
		if kruskal(i, graphAux):
			trees.append(i)
			counter+=1 
	
	finalTrees = Tree()
	finalTrees.colors = createColors(len(Kgraph.vList))
	for i in trees:
		tree = Graph()
		for j in range(len(i)+1):
			vertex = Vertex()
			vertex.id = j
			vertex.color = finalTrees.colors[j]
			tree.vList.append(vertex)
		for e in i:
			tree.vList[Kgraph.eList[e].u.id].neighbors.append(tree.vList[Kgraph.eList[e].v.id])
			tree.vList[Kgraph.eList[e].v.id].neighbors.append(tree.vList[Kgraph.eList[e].u.id])
			tree.eList.append(Kgraph.eList[e])
		finalTrees.treesList.append(tree)	
				

					
	return finalTrees

def upColor(arrayColors, colors):
	i = 0
	for c in colors:
		arrayColors[i].color = c
		i+=1 

def createColors(k):
	colors = []
	for i in range(k):
		color = Color(i)
		colors.append(color)
	return colors	

def kruskal(index, graph):
	for i in index:
		u = graph.eList[i].u
		v = graph.eList[i].v 
		
		if find(u) == find(v):
			return False
		union(u, v)

	return True


def union(u, v):
	p = find(u)
	q = find(v) 	
	p.representative = q

def find(u):
	if u.id == u.representative.id:
		return u	
	return find(u.representative)						
