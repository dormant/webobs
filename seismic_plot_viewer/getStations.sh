#!/usr/bin/bash

#cat holdings.txt | awk '{print $2}' | sort -u > stations.txt

while read p; do
#  echo "$p"
    grep "^$p" ~/STUFF/data/seismic/SeismicStations/data/names.txt | sed '0,/,/s//:/'
done <stations.txt
