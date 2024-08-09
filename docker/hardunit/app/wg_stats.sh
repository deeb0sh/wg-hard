#!/bin/bash

i=1
n=0
printf "{\n"
exec < <(exec wg show wg0 dump)
while read -r out; do
  ((n >= i )) &&  echo $out | (IFS='	 ' read -r x1 x2 x3 x4 x5 x6 x7 x8 x9 x10; echo -e "\t{\n\t\t\"last\": $x5,\n\t\t\"tx\": $x6,\n\t\t\"rx\": $x7,\n\t}," )
  ((n++))
done
printf "}"
