#!/bin/bash
num_clients=${NUM_CLIENTS:-5}
for ((i=0; i<num_clients; i++))
do
  python client.py $i &
done
wait
