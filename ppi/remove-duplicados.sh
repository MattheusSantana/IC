#!/bin/bash

# script não está ok: deve remover duplicados apenas para um mesmo motif buscado, não para todos entre si

cksum $@ | sort -n > sums.txt

old=""
while read sum lines filename
do
  if [[ "$sum" != "$old" ]]
  then
    old="$sum"
    continue
  fi
  echo "removing $filename"
  #rm -f "$filename"
done < sums.txt

#rm sums.txt

exit 0

