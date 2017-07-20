#!/bin/bash

docker login
docker pull alpine
docker tag alpine:latest registry.example.com:5000/my-alpine
docker push registry.example.com:5000/my-alpine
