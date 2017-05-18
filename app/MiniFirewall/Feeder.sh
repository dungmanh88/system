#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage $0 input_file filter"
  exit -1
fi

if [ -z $1 ]; then
  echo "Empty first param"
  exit -1
fi

if [ -z $2 ]; then
  echo "Empty second param"
  exit -1
fi

input=$1
echo $input
filter_str=$2
echo $filter_str

output="unique_ip_by_filter_str"

while true; do
  cat $input | grep -F $filter_str | cut -d " " -f 1 | sort | uniq > $output
  sleep 5
done
