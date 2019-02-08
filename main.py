import timeit
import sys
from graph import *
from makeGraph import *
from tcg import *
from operator import attrgetter
import copy
import os
import argparse


'''
parser = argparse.ArgumentParser(description='Search Motifs in Metabolic Networks.')
parser.add_argument("-o", "--operation", choices=['-T', '-E', '-C'], help='Operation: -T : Decide if the motif occurs in the network. -E : Enumerate all isomorphics occurrences of the motif in the network.\n\n -C : Count the number of occurrences of a motif.')
parser.add_argument('-D', '--directory', help='Directory containing graphs and motifs files.')
parser.add_argument('-G', '--graph', help='Biological network graph.')
parser.add_argument('-M', '--motif', help='Motif (Protein Complex).')
parser.add_argument("-B", "--build", help='build graphs and motifs file. See -h -B for tutorial.')
parser.add_argument('-m', '--maximum', type=int, help='Limit the number of occurrences found. Must be used with -E.')
parser.add_argument('-gl', '--localGaps', help='To allow local gaps in the occurrences.')
parser.add_argument('-nl', type=int, help='Number of local gaps allowed in the occurrences. Must be used with -gl. Default is zero.')
parser.add_argument('-e', '--evalue', help='List sum of e-values of occurrences.')
parser.add_argument('-v', '--verbose', help='Verbose mode.')
parser.add_argument('-i', '--input', help='Show format of input files.')
parser.parse_args()
'''
#parser.add_argument('-h -B', help=tutorial[0])

#tutorial[0] = "Graph and motif files are built from ..."




directory = sys.argv[1]		
files = os.listdir(directory)	
total = 0
founds = []
nfounds = []
newFounds = 0
notAllColors = []
numberMax = []
result = 0

totalDuplicatedVertex = 0
totalGlobalOccurrences = 0

#It receives a directory containing several graph and motif files and returns an ordered list of graphs and their respective motifs.
#Check if all colors in the motif are in the graph.
#Verifies if the motif size is less than limit passed in the argument list.
def managerFiles(files):
	exceedsSize = []
	noAllColors = []
	maxMotifSize = 5
	match = []
	counter = 0
	print("[INFO]: Preparing files")
	for file in files:
		if "motif_" in file:
			counter+=1
			motifAddress = directory+file
			graphName = file.replace("motif", "graph")
			
			#Verifies motif size.
			motif = open(motifAddress, 'r')
			motifSize = int(motif.readline())
			
			if maxMotifSize < motifSize or motifSize == 1:
				print("[REMOVED]:", graphName,"The size of the motif has exceeded the parameter limit", end="\r")
				exceedsSize.append(graphName)
				continue
			

			graphAddress = directory+graphName

			graph = makeGraphPPI(graphAddress)
			graph.initializeColorTable()

			
			colors = list(range(1, motifSize, 1))


			if checkAllColors(graph, colors) == False:
				print("[REMOVED]:",graphName, "The graph does not have all the colors of the motif...", end="\r")
				noAllColors.append(graphName)
				continue
			match.append((graphAddress, motifAddress))


			

	motif.close()	
	match.sort()	
	print("\n[INFO]: %d graphs of %d have been removed!"%((len(exceedsSize) + len(noAllColors)), counter))	
	return match, exceedsSize, noAllColors

def getNumberOfVertices(fileMotif):
	return int(fileMotif.readline()) #Getting number of vertices in the first line.

def handle(match):
	totalDuplicatedVertex = 0
	totalGlobalOccurrences = 0
	totalGlobalFound = 0
	for m in match:
		# if numero de vértices for menor do que o passado por parametro 
		# if enumerate :	
		
		#print(m[0])  #Print graph Addres
		aux1, aux2, found = enumerate(m[0], m[1])	
		
		if aux1 > 0:
			totalDuplicatedVertex += aux1
			totalGlobalOccurrences += aux2
			print("[INFO]: %d of %d occurrences were removed by duplicated vertices."%(aux1, aux2))

		if found > 0:
			totalGlobalFound+=1	
	print("[INFO]: %d of %d occurrences were removed by duplicated vertices."%(totalDuplicatedVertex, totalGlobalOccurrences))
	print("[RESULT]: %d motifs of %d were found." %(totalGlobalFound, len(match)))

def enumerate(graphAddress, motifAddress):
	maxoccurrences = 5000
	partition = list(graphAddress.split("/"))
	graphName = partition[-1]
	motifs = makeAllMotifsPPI(motifAddress) #Generate All motif topologies 
	allOccurrences = []
	totalDuplicatedVertex = 0
	totalGlobalOccurrences = 0

	for m in motifs:

		graphCopy = makeGraphPPI(graphAddress)
		result =  TCG(graphCopy, m)
		
		if result < 1:
			continue		
		
		cleangraph = cleargraph(graphCopy, m)	
		occurrences = allIsomorphics(cleangraph, m)
		totalGlobalOccurrences += len(occurrences)
		
		length = len(occurrences)
		for i in range(length-1,-1, -1):
			if checkDuplicatedVertex(occurrences[i]) == True:
				del(occurrences[i])
				totalDuplicatedVertex+=1
					
		
			
		
		
		allOccurrences += occurrences 
	if len(allOccurrences) > 0:
		
		#Removing occurrences with duplicated vertices.

		oldLength = len(allOccurrences)
		allOccurrences = checkEqualsOccurrences(allOccurrences)	
		newLength = len(allOccurrences)
		removed = oldLength - newLength
		if removed > 0:
			print("[INFO]: %d of %d occurrences were removed because they were the same"%(removed, oldLength))


		for occurrence in allOccurrences:
			sumEvalue(occurrence)
	


		allOccurrences.sort(key=attrgetter("totalEvalue"))
		printAllOcurrences(allOccurrences, graphName)
		
	return totalDuplicatedVertex, totalGlobalOccurrences, len(allOccurrences)



def checkEqualsOccurrences(allOccurrences):
	dic = {}
	for graph in allOccurrences:
		label = ""
		graph.vList.sort(key=attrgetter("label"))

		for protein in graph.vList:
			label+=protein.label
		dic[label] = graph
		
	return list(dic.values())



def printAllOcurrences(allOccurrences, graphName):

	print("[RESULT]: %d occurrences found in %s" %(len(allOccurrences),graphName))
	for graph in allOccurrences:
		for v in graph.vList:
			print(v.id , v.label, v.evalue)		
		print("Total e-value:",graph.totalEvalue,"\n")
	print("\n")	

#TO DO 
def writeoccurrences(occurrences, fileName):
	arch = open(fileName, 'w')
	if (arch == None): 
		print("[INFO]: Could not open file")


	arch.write(fileName)
	arch.write("\n")
	for occurrence in occurrences:
		for v in occurrence.vList:
			arch.write(v.label)
			arch.write("\n")
		arch.write("\n")


def cleargraph(graph, motif):
	#Clear graph of enumerate occurrences.
	for v in graph.vList:
		v.status = V_ENABLE
	cleargraph = cleanGraphVertices(graph,motif)
	cleanGraphEdges(cleargraph, motif)
	return cleargraph

def printlogs():						
	print("Founds")
	for g in founds:
		print(g) 		

	print("Not Founds")
	for g in nfounds:
		print(g) 		

	print("without colors")
	for g in notAllColors:
		print(g) 		

	print("greater than 7")
	for g in numberMax:
		print(g)	


match, exceedsSize, noAllColors = managerFiles(files)
handle(match)


'''
	TO DO:
	- Fazer TCG para todas as topologias de um motif.

	- Texto de inicialização, explicando o funcionamento do software.
	- fazer argparse para o ppinew.
	- Opção de buscar um determinado motif em uma rede, passados por comando.
	- Se for verboso imprimir a topologia.
	- Se tiver gap, listar onde deve ser colocado o gap.
'''

