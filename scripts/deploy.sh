#!/usr/bin/env bash
set -ev

VERSION=$(git describe --tags)
IMAGE_NAME=kinaklub/next.filmfest.by:$VERSION

docker build -t $IMAGE_NAME .
docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker push $IMAGE_NAME
