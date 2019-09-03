#!/bin/bash

# Launch Apache Server
echo "Starting Apache Server"
OUTPUT="$(service apache2 start)"
echo "${OUTPUT}"

# Start Scanning Loop
#echo "Starting Scanning Loop"
#while true
#do
#    OUTPUT="$(python3 main.py)"
#    echo "${OUTPUT}"
#    sleep 180
#done

OUTPUT="$(python3 main.py)"
echo "${OUTPUT}"

while true
do
    echo "Scanning Alive"
    sleep 60
done
