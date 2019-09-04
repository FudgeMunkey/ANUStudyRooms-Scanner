#!/bin/bash

APP="anusr-scanner-image"

docker build -t ${APP} .

docker-compose up -d
