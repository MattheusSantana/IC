#!/bin/bash
#
# Example:
#   mkdir graphs
#   ./generate-graphs-motifs.sh ../../tools/ppi2cgraph.py ppi/Yeast\ \(Saccharomyces\ cerevisiae\).ppi fasta/Yeast\ \(Saccharomyces\ cerevisiae\).fasta fasta/Bovine.fasta motifs/Bovine\ Complexes\ CORUM.txt graphs
#

if [ $# -ne 6 ]
then
  echo "$0 <ppi2cgraph.py_location> <ppi_file> <network_fasta> <query_fasta> <motifs_file> <output_dir>"
  exit 1
fi

ppi2cgraph="$1"
ppifile="$2"
networkfasta="$3"
queryfasta="$4"
file="$5"
outdir="$6"

count=0

while read -d $'\t' name
do
  echo "#$count: $name"
  read -d $'\n' line
  proteins=($line)

  if [ ${#proteins[@]} -lt 1 ]
  then
    echo "*No proteins in line: $name"
    echo
    continue
  fi

  n=$(printf %03d $count)
  #echo "$ppi2cgraph" -q -i "$ppifile" -f "$networkfasta" -F "$queryfasta" -g "$outdir/graph_${n}.txt" -t "$outdir/motif_${n}.txt" ${proteins[@]}
  "$ppi2cgraph" -q -i "$ppifile" -f "$networkfasta" -F "$queryfasta" -g "$outdir/graph_${n}.txt" -t "$outdir/motif_${n}.txt" ${proteins[@]}
  if [ $? -ne 0 ]
  then
    echo "!!ERROR processing proteins (maybe some of them are not in $queryfasta)!!"
    rm -f "$outdir/graph_${n}.txt" "$outdir/motif_${n}.txt" > /dev/null 2>&1
  else
    echo ${#proteins[@]} > "$outdir/motif_${n}.txt"
    seq -s ',' 1 ${#proteins[@]} >> "$outdir/motif_${n}.txt"
    echo "${proteins[@]}"  >> "$outdir/motif_${n}.txt"
    echo "OK!"
  fi
  let count++
  echo
done <<< "$(cat "$file" | sed "s/\r//" | grep -v '^$')"


