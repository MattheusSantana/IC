import timeit
import sys
from graph import *
from makeGraph import *
from tcg import *
import copy
import os
sys.setrecursionlimit(10000000)

					
def main():
	args = list(sys.argv)

	directory = sys.argv[2]		
	files = os.listdir(directory)	
	total = 0
	for file in files:
		if "motif_" in file:
			motifAddress = directory+file 					#Getting motif address
			graphName = file.replace("motif", "graph")		#Getting adress of the graph relating to the motif.

			#Open motif file
			motifAddress = open(motifAddress,'r')
			firstline = int(motifAddress.readline())
			if firstline >2 and firstline< 7:
				#Open graph file and making graph.
				graph = makeGraphPPI(directory+graphName)
				#Generating all the different topologies for the motif.
				motifs = makeAllMotifsPPI(directory+file)
				motiffounds = 0
				print(graphName)
					
				#Search with TCG Algorithm.
				if sys.argv[1]	== '-T':
					if  '-v' in args:
						for m in motifs:
							result =  TCG(graph, m)
							if result == 1:
								if '-G' in sys.argv:
									setGap(graph, motifs[0])
						
								print("File:",file,"|"," The motif has been found!")
								
								
								m.printArchiveMode()	
								
								for v in graph.vList:
									v.status = V_ENABLE
								g = cleanGraphVertices(graph,m)
								cleanGraphEdges(g, m)
								
								graphs = allIsomorphics(g, m)
								
								print("Total Found:",len(graphs),"\n")
								for graph in graphs:
									graph.printArchiveMode()
									print("\n")
								total+=1
								break
						if result != 1:
							print("File:",file,"|"," No topology was found!")
					else:
						for m in motifs:
							result =  TCG(graph, m)
							if result == 1:
								total+=1
								break
						#print("Searching motifs, please wait a sec! Total motifs Founds: ",total, end="\r")
				if sys.argv[1] == '-C':
					graph.initializeColorTable()
					if '-v' in args:
						for m in motifs:
							qtd = countOcurrences(graph, m)
							if qtd > 0:
								total+=1
								print("File:",file,"|"," The motif has been found!", "|", "Motif size:",len(m.vList), "| Total ocurrences: ",qtd)
								
								break
						if qtd == 0:
							print("File:",file,"|"," No topology was found!")
					else:
						for m in motifs:
							qtd = countOcurrences(graph, m)
							if qtd > 0:
								total+=1
								break
						print("Searching motifs, please wait a sec! Total motifs Founds: ",total, end="\r")	
					
										
								
	print("\nTotal founds", total)					
						
				
main()				