#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -d -p 5000:5010 \
  --name=${app} \
  -v $PWD:/app ${app}
