#!/usr/bin/env bash
set -ev

VERSION=$(git describe --tags)
export IMAGE_NAME=kinaklub/next.filmfest.by:$VERSION

echo $TRAVIS_SECRET | gpg --passphrase-fd 0 .docker/ca.pem.gpg
echo $TRAVIS_SECRET | gpg --passphrase-fd 0 .docker/cert.pem.gpg
echo $TRAVIS_SECRET | gpg --passphrase-fd 0 .docker/key.pem.gpg

export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://207.154.195.49:2376"
export DOCKER_CERT_PATH=".docker"

docker stack deploy -c docker-stack.yml next
