#!/bin/bash

host=$1
port=$2
command=$3

if [ -z $host ]; then
  echo "I need host"
  exit 1
fi

if [ -z $port ]; then
  echo "I need port"
  exit 1
fi

while true
do
  nc $host $port < /dev/null &> /dev/null
  result=$?
  if [ $result -eq 0 ]; then
    echo "The connection to $host:$port is ready"
    if [ -z "$command" ]; then
      break
    fi
    echo "Test command: $command"
    eval "$command" &> /dev/null
    result=$?
    if [ $result -eq 0 ]; then
      echo "Run command: $command successfully"
      break
    fi
  fi
  echo "Waiting..."
  sleep 5
done
echo "Connection to $host:$port is successful"
