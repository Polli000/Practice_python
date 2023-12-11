#!/bin/bash

# create the network
docker network create elastic

# pull elasticsearch build and run it
docker run --name elastic --net elastic -d -p 9200:9200 -p 9300:9300 --rm -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.2.3

# build the flask container
docker build -t intern-task:latest .

# start the flask app container
docker run --name api-app --net elastic -d -p 5000:5000 --rm intern-task:latest