#!/bin/bash

# Launch Apache Server
echo "Starting Apache Server"
OUTPUT="$(service apache2 start)"
echo "${OUTPUT}"

# Start Scanning Loop
echo "Starting Scanning Loop"
while true
do
    OUTPUT="$(python3 main.py)"
    echo "${OUTPUT}"
    sleep 900
done


