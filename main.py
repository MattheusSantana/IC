import timeit
import sys
from graph import *
from makeGraph import *
from tcg import *
import copy
import os

# 1 Step: make K-graph
# 2 Step: make trees 
# 3 Step: print trees and search
# 4 Step: save motifs and not motifs
'''
directory = sys.argv[2]
ocurrences = 0
files = os.listdir(directory)
for f in files:


	#taking motifs only.
	if "motif_" in f:
		
		arch = directory+f
		graphName = f.replace("motif", "graph")
		
		archive = open(arch,'r')
		#reading the first line
		firstline = int(archive.readline())
		if  firstline <7:
			
			#Open the graph.
			
			graph = makeGraphPPI(directory+graphName)
			motifs = makeAllMotifsPPI(arch)
			graph.initializeColorTable()
			
			
			
			
			for m in motifs:
				qtd = countOcurrences(graph, m)
				i+=1
				#print(i,"->", qtd)
				if qtd > 0:
					print(f, "->", firstline)
					#print("achou ->", qtd )
					ocurrences+=1
					break	
			
			for m in motifs:
				i+=1
				#print(i)
				if TCG(graph, m) == 1:
					ocurrences+=1	
					print(f.replace(".txt","\n"),end="")
					m.printArchiveMode()
					break'''
					
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
			if firstline <7:
				#Open graph file and making graph.
				graph = makeGraphPPI(directory+graphName)
				#Generating all the different topologies for the motif.
				motifs = makeAllMotifsPPI(directory+file)
				motiffounds = 0
				
				#Search with TCG Algorithm.
				if sys.argv[1]	== '-T':

					
					if  '-v' in args:
						for m in motifs:
							result =  TCG(graph, m)
							if result == 1:
								print("Searching:",file,"|"," The motif has been found!")
								total+=1
								break
						if result != 1:
							print("Searching:",file,"|"," No topology was found!")
					else:
						for m in motifs:
							result =  TCG(graph, m)
							if result == 1:
								total+=1
								break
						print("Searching motifs, please wait a sec! Total motifs Founds: ",total, end="\r")
					
	print("\nTotal founds", total)					
main()				
							