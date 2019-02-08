#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
#   Copyright (C) 2015 Diego Rubert, Elói Araújo and Marco A. Stefanes
#   
#   This file is part of SIMBio.
#   
#   SIMBio is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   SIMBio is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with SIMBio. If not, see <http://www.gnu.org/licenses/>.
#

'''
Generates a colored graph and a colorful motif (without edges) from PPI network
'''

import argparse
import re
from Bio.Blast.Applications import NcbiblastpCommandline


##### PARSER #####
parser = argparse.ArgumentParser(description = __doc__, formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="\
Ex.:\n\n\
  ppi2cgraph.py -i file.ppi -f file.fasta -F fileq.fasta -g graph.txt -t motif.txt YAL001C YBR123C YAL002W\n\n\
PPI file format ex.:\n\
  YLR447C YOR332W 0.126299948542569\n\
  YPL084W YPR173C 0.952299123053322\n\
  ...\n ")
parser.add_argument('-i', dest='ppi_fname', metavar="file.ppi", help='input PPI file', required=True)
parser.add_argument('-f', dest='fasta_fname', metavar="file.fasta", help='input FASTA file (contains protein sequences)', required=True)
parser.add_argument('-F', dest='fastaq_fname', metavar="fileq.fasta", help='input FASTA file for query proteins (may be the same of -f)', required=True)
parser.add_argument('-g', dest='graph_fname', metavar="graph.txt", help='output file defining the graph', required=True)
parser.add_argument('-t', dest='tree_fname', metavar="motif.txt", help='output file defining the colorful tree (without edges)', required=True)
parser.add_argument('-T', dest='threshold', metavar="threshold", help='threshold considered for interaction probability ([0.0..1.0], default: 0.0)', default=0.0, required=False)
parser.add_argument('-E', dest='evalue', metavar="e-value", help='BLAST threshold for E-value ([1e-99..1e-3], default: 1e-7)', default=1e-7, required=False)
parser.add_argument('-v', '--verbose', dest='verbose', help='verbose mode', default=False, required=False, action="store_true")
parser.add_argument('-q', '--quiet', dest='quiet', help='quiet mode', default=False, required=False, action="store_true")
parser.add_argument('-nu', '--nouncolored', dest='nouncolored', help='it will not include uncolored vertices', default=False, required=False, action="store_true")

parser.add_argument('query', metavar='PROT', type=str, nargs='+', help='Proteins for motif search')
options = parser.parse_args()
##################


##### VAR INITIALIZATION #####
verbose = options.verbose
quiet = options.quiet
nouncolored = options.nouncolored

if verbose and quiet:
  print "How can I be verbose and quiet?"
  exit(1)

threshold = float(options.threshold)
evalue = float(options.evalue)
fppi = open(str(options.ppi_fname), 'r')
ffasta = open(str(options.fastaq_fname), 'r')
ftree = open(str(options.tree_fname), 'w')
fgraph = open(str(options.graph_fname), 'w')

##### DEFINE COLORS AND WRITE MOTIF FILE #####
color = {}
ncolors = 1
ftree.write("%d,%d\n" % (len(options.query), len(options.query)+1)) # number of vertices and colors
for p in options.query:
  if not quiet: print "color %d: %s" % (ncolors, p)
  ftree.write("%d:%d %s\n" % (ncolors-1, ncolors, p)) # each vertex with it's color and label
  color[p] = ncolors
  ncolors += 1
if not quiet: print "color 0: everything else", "\n" if verbose else ""
ftree.close()

##### PARSE PPI FILE #####
n = 0
m = 0
vertices = {} # we could use list, but for this network dict will be easyer
added = set()
for line in fppi:
  (name1, name2, prob) = line.split()
  prob = float(prob)

  for name in name1, name2:
    if not vertices.has_key(name):
      vertex = {}
      vertex["id"] = n
      vertex["label"] = name
      vertex["evalue"] = []
      vertex["colors"] = []
      vertex["edges"] = []
      n += 1
      vertices[name] = vertex

  v1 = vertices[name1]
  v2 = vertices[name2]
  if prob >= threshold:
    v1["edges"].append(v2["id"])
    v2["edges"].append(v1["id"]) # but we don't write to file 2 times
    if verbose:
      print "%d-%d (%f)" % (v1["id"], v2["id"], prob)

##### ALIGN AND ADD COLORS TO PROTEINS #####
fasta = ffasta.read()
for p in options.query:
  match = re.search(r">"+p+"\n([ \nA-Z]*)[*>]", fasta)

  if not match or len(match.groups()) < 1:
    match = re.search(r">"+p+"\n([ \nA-Z]*)$", fasta) # maybe it's the last
    if not match or len(match.groups()) < 1:
      print "Protein %s sequence not found in fasta file %s" % (p, options.fastaq_fname)
      exit(1)
    
  query = match.group(1).replace('\n','')
  blastp_cline = NcbiblastpCommandline(subject=str(options.fasta_fname), outfmt="'6 sseqid evalue'")
  out, err = blastp_cline(stdin=query)
  if err:
    print err
  
  for line in out.splitlines():
    subject,e = line.split()
    e = float(e)
    if not vertices.has_key(subject): # sometimes the protein in fasta isn't in network
      continue
    v = vertices[subject] # this is easy just because we are using dicts
    if e < evalue and not color[p] in v["colors"]:
      v["colors"].append(color[p])
      v["evalue"].append(e)  #add e-value in vertex.
      if verbose:
        print "%s: color %d (%s), evalue: %g" % (v["label"], color[p], p, e) 


# now that the dict isn't needed anymore, we sort vertices by id obtaining a list
vertices = sorted(vertices.values(), key=lambda x: x["id"])

# white color for vertices uncolored
for v in vertices:
  if len(v["colors"]) == 0:
    v["colors"].append(0)
    if verbose:
      print "%s: color 0 (NONE)" % v["label"]
      
# duplicate multicolored vertices
for v in vertices:
  if len(v["colors"]) > 1 and verbose:
    print "Duplicating %d (%s): colors %s" % (v["id"], v["label"], ','.join([str(x) for x in v["colors"]]))
  while len(v["colors"]) > 1: # for each color after first
    color = v["colors"][1] # second color
    ev = v["evalue"][1] # second evalue
    copy = v.copy() # this doesn't copy colors and edges lists
    copy["id"] = n
    copy["colors"] = [color] # a new list
    copy["evalue"] = [ev]
    copy["edges"] = v["edges"][:] # a copy, not reference

    v["colors"].remove(color)
    v["evalue"].remove(ev)
    for i in copy["edges"]:
      vertices[i]["edges"].append(copy["id"])
    vertices.append(copy)
    n += 1

oldlength = len(vertices)
if nouncolored:
  
  for i in range(len(vertices)-1, -1, -1):
    if 0 in vertices[i]["colors"]:
      del(vertices[i])
  
  if verbose:
    print "\n%d uncolored vertices were removed."%(oldlength - len(vertices))



##### WRITE NETWORK FILE #####
fgraph.write("%d,%d\n" % (n, ncolors)) # number of vertices and colors
for vertex in vertices:
  if vertex["evalue"] != None :  
    fgraph.write("%d:%d %s %g\n" % (vertex["id"], vertex["colors"][0], vertex["label"], vertex["evalue"][0])) # now each vertex has just 1 color

for vertex in vertices:
  for id in vertex["edges"]:
    if id > vertex["id"]:  # to guarantee we just add edges 1 time, just forward edges
      fgraph.write("%d-%d\n" % (vertex["id"], id)) # each edge
      m += 1

if not quiet: print "\nNetwork graph: %d vertices and %d edges" % (n, m)

if not quiet: print "\n***** PLEASE, ADD EDGES IN TREE (MOTIF) FILE: %s *****\n" % options.tree_fname
exit(0)

