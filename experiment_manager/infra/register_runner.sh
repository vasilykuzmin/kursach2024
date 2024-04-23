#!/usr/bin/env bash

source ./.env

docker exec -it infra-gitlab-runner-1 \
  gitlab-runner register \
    --non-interactive \
    --token $1 \
    --url "http://gitlab" \
    --executor shell \
    --docker-network-mode gitlab-network
