#!/bin/sh
docker container prune -f
docker image prune -a -f