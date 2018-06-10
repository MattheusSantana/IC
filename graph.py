V_ENABLE = 1
V_DISABLE = 0

class Vertex(object):
	def __init__(self):
		self.id = 0
		self.color = 0
		self.status = V_ENABLE
		self.degree = 0
		self.label = ""			
		self.neighbors = []		#Adjacents vertices
		self.ecNumber = 0 		#not being used for now
		self.brand = V_ENABLE	#it may be that you participate in a motif
		self.level = 0			#discovery time of DFS 
		self.successors = {}
		self.value = 1
		self.representative = self
	
	def printNeighbors(self):
		print("%d  {"%(self.id), end="")
		for neighbor in self.neighbors:
			print("----> %d"%( neighbor.id), end=" ")

		print("}")	
	

	def isAdjacent(self, i):
		for x in self.neighbors:
			if x.id == i:
				return 1
		return 0	

	def printSuccessors(self):
		print(self.id, "|", self.value, "--> {", end=" ")
		for successor in self.successors:
			print("-->",successor.id, end=" ")	
		print("}")

class Edge(object):
	def __init__(self):
		self.u = None
		self.v = None

	def printEdge(self):
		print("%d-%d"%(self.u.id, self.v.id))	
		
class Tree(object):
	def __init__(self):
		self.treesList = []
		self.colors = []		
class Graph(object):
	def __init__(self):
		self.n = 0	        # Number of vertices 
		self.ocurrences = 0 # Number of ocurrences
		self.maxN = 0		# Max number of vertices
		self.maxColor = 0	# Max number of colors
		self.vList = []		# List of vertices
		self.topologicalSort = []
		self.level = 0
		self.colorTable = [] 
		self.map = []
		self.eList = []		#List of edges
		self.eTuple = []	#List of edges in tuple format.
		self.colors = [] #List of the all colors.
	def printVertices(self):
		print(len(self.vList))
		for vertex in self.vList:
			print(vertex.id, vertex.color, vertex.label)	
			
	def printArchiveMode(self):
		n = len(self.vList)
		print(n)
		i = 0
		if n == 1:
			print("%d:%d %s"%(self.vList[i].id,self.vList[i].color, self.vList[i].label))
		else:
			for i in range(n-1):
				print("%d:%d %s"%(self.vList[i].id, self.vList[i].color, self.vList[i].label))			
			print("%d:%d %s"%(self.vList[i+1].id, self.vList[i+1].color, self.vList[i+1].label),end="")
		self.printEdges()

	def printAdjacents(self):
		for vertex in self.vList:
			vertex.printNeighbors()	
	def printEdges(self):
		for edge in self.eList:
			edge.printEdge()	
		print("")		
		#print("Total Edges:", len(self.eList))	

	
	#A Simple depth-first search
	def dfs(self):
		for vertex in self.vList:
			vertex.status = V_ENABLE
		
		for vertex in self.vList:
			if vertex.status == V_ENABLE:
				self.dfsVisit(vertex)

	#2 step of depth-first search	
	def dfsVisit(self, vertex):
		vertex.status = V_DISABLE
	
		for neighbor in vertex.neighbors:
			if neighbor.status == V_ENABLE:
				vertex.successors[neighbor.color] = 0
				self.dfsVisit(neighbor)

		vertex.level = self.level		
		self.level +=1
		self.topologicalSort.append(vertex)


	def initializeColorTable(self):
		length = self.maxColor
		for i in range(length):	
			vector = []
			self.colorTable.append(vector)

		for x in self.vList:
			self.colorTable[x.color].append(x)

	def printColorTable(self):
		length = len(self.colorTable)
		for i in range(length):
			print(i, "{", end="")
			for vertex in self.colorTable[i]:
				print("->",vertex.id, end = " ")
			print("}")						

