#!/bin/bash

#set -e

if [ $# -lt 1 ]
then
  exit 1
fi

# criando arquivos com todos motifs
for i in $@
do
  egrep -v "^$|TOTAL: 0 |\.local\]|TOPOLOGICAL MOTIFS|real.*s$|user.*s$|sys.*s$|TOTAL OF COMB|/data/|mpirun|------" "$i" | sed "s/@@@@TOTAL.*//" > "motifs-${i##*/}"
done

# criando estrutura de pastas
for i in fly human yeast
do
  mkdir "$i"
  for j in bovine mouse rat
  do
    mkdir "$i/$j"
  done
done

# criando arquivos separados para cada motif
count=0
count2=0
for i in motifs-*.txt
do
  while read line
  do
    if [ -z "$line" ]
    then
      if [ $count2 -gt 0 ]
      then
        let count++  
      fi
      count2=0
    else
      n="$(printf "%06d" $count)"
      m="$(printf "%05d" $count2)"
      j="${i#motifs-}"
      a="${j%-*}"
      b="${j#*-}"
      b="${b%.txt}"
      echo -e "${line// /\\n}" > "$a/$b/$n-$m.txt"
      let count2++
    fi
  done < "$i"
done

# removendo duplicados e compactando
# não remove duplicados pois essa checagem está sendo feita no simbio
for i in fly human yeast
do
  cd "$i"
  for j in bovine mouse rat
  do
    cd "$j"
    find . -iname "*.txt" -exec sort '{}' -o '{}' \;
    #../../remove-duplicados.sh *.txt
    zip -r9 "$i-$j.zip" *.txt
    mv "$i-$j.zip" ../../
    cd ..
  done
  cd ..
done

# removendo arquivos temporarios
rm -rf fly human yeast motifs-*.txt

exit 0
