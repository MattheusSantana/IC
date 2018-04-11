import time
from graph import * 


#search for an instance of the motif in the graph
def TCG(graph, motif):
		motif.dfs()
		for i in range(len(motif.topologicalSort)):
			v = motif.topologicalSort[i]
			A = []
			w = None
			for a in graph.vList:
				if a.status == V_ENABLE and a.color == v.color.color:
					A.append(a)
			
			w = v.neighbors[0]

			#selecting neighbor that has a level greater than vertex v to maintain the order of dfs.
			for neighbor in v.neighbors:
				if(neighbor.level > v.level):	
					w = neighbor
					break
			

			if(i == len(motif.topologicalSort)-1):
				graph.map.append(v)
				if(len(A) == 0):
					print("No occurrences")
					return;
				else:
					print("The motif occurs in the graph")
					return;	

			graph.map.append(w)
		
			for b in graph.vList:
				if b.status == V_ENABLE and b.color == w.color:
					if adjTo(b,v) == 1:
						graph.vList[b.id].brand = V_DISABLE
						graph.vList[b.id].status = V_DISABLE

			for a in graph.vList:
				if a.status == V_ENABLE and a.color == v.color.color:
					graph.vList[a.id].status = V_DISABLE			
#It says if two vertices are adjacent
def adjTo(x, w):
	for vertex in x.neighbors:
		if(vertex.status == 1 and vertex.color == w.color.color):
			return 0
	return 1	

def ocurrence(self, array, motif):
	aux = self.map[-1]

	#Obtaining leaf belonging to a motif
	for v in self.vList:
		if v.brand == V_ENABLE and v.color == aux.color:
			#Adding vertex on ultimate position of array.
			array[-1] = v
			break
	for i in range(len(self.map)-2, -1, -1):
		
		index =  self.map[i].level
		
		vertex = array[index]
		color = motif.topologicalSort[i].color
		
		
		for neighbor in vertex.neighbors:
			if neighbor.brand == V_ENABLE and neighbor.color == color:
				array[i] = neighbor
				break	

	#Print the ocurrence
	print("Ocurrence:", end="")
	for i in range(0, len(array), 1):
		print(array[i].id, end=" ")
					

def proxSeq(self, l, n):
    i = len (l) - 1
    x = n - 1
    while i >= 0 and l[i] == x: 
       i -= 1
       x -= 1
    if i == -1: return 0
    x = l[i] + 1
    while i < len(l):
   	   l[i] = x
   	   x += 1
   	   i += 1
    return 1

def subsets(self, l, n):
	while(self.proxSeq(l,n)== 1):
		for i in range(1, len(l), 1):
			if not self.vList[l[0]].isAdjacent(l[i]):
				print(self.vList[l[0]].id, l[i])
				#Adding edges in the vertex 
				self.vList[l[0]].neighbors.append(self.vList[l[i]])
				self.vList[l[i]].neighbors.append(self.vList[0])
		
		print("")	

def printSuccessors(self):
	for vertex in self.vList:
		print("Vertice => ", vertex.id, "-> {", end="")
		for key in vertex.successors.keys():
			print("->", key, ":", vertex.successors.get(key), end=" ")
		print("}")	


#1 - For each m vertex of the motif in the topological sort.
#2 - For each v vertex of the graph with the same color as m.
#3 -v receives the same successors as m.
#4 -For each neighbor of v who is also a successor of v.
#5 -Increase the neighbor / successor value in your respective key.
#6 -Multiply the key values such that the total value of v is the result of this multiplication.
#7 -The last calculated result will be the printed output.
def countOcurrences(graph, motif):
	
	for m in motif.topologicalSort:
		
		result = 0 # Will save the final result
		
		for v in graph.colorTable[m.color.color]:
			
			v.successors = m.successors.copy()

			for neighbor in v.neighbors:
				if v.successors.get(neighbor.color) != None:
					v.successors[neighbor.color] += neighbor.value

			total = 1		
			for key in v.successors.keys():
				total *= v.successors.get(key)
			v.value = total
			result += total
	#print("Total Ocurrences: ",result)	
	for m in motif.topologicalSort:
		for v in graph.colorTable[m.color.color]:
			v.value = 1
			v.successors.clear()
	return result

#Initializing graph that be populated.


#motif = Graph()

#motif.CreateMotif("motif-600.txt")
#motif.CreateMotif("motif-3.txt")

# ------------> Creating subsets <----------
#graph.subsets(list(range(2)), len(graph.vList))


''' ------> Calling the TCG function <--------
motif.dfs()
graph.TCG(motif)
'''	


''' ------> Getting an occurrence <-----------
motif.dfs()
graph.TCG(motif)

#save an occurrence.
v = [None] * len(motif.vList)
graph.ocurrence(v, motif)
'''


#---> Counting the number of occurrences <----
'''
motif.dfs()
graph.initializeColorTable()
inicio = time.time()
countOcurrences(graph, motif)
fim = time.time()
print("%0.9f" %(fim - inicio))
'''

