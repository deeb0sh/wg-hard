#!/bin/bash

i=1
n=0
printf "["
exec < <(exec wg show wg0 dump)
while read -r out; do
      ((n >= i )) &&  echo $out | (IFS='         ' read -r x1 x2 x3 x4 x5 x6 x7 x8 x9 x10; printf "{\"last\": $x5,\"tx\": $x6, \"rx\": $x7},")
      ((n++))
done
printf "]"
