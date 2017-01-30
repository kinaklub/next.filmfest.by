#!/usr/bin/env bash
set -ev

VERSION=$(git describe --tags)
export IMAGE_NAME=kinaklub/next.filmfest.by:$VERSION

docker build -t $IMAGE_NAME .

if [ ! -z "$DOCKER_USERNAME" ]
then
   docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
fi

docker push $IMAGE_NAME
