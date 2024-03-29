#!/bin/bash
docker stop -t 1 $(docker ps -aq)
docker rm $(docker ps -aq)

