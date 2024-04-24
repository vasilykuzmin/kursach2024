#!/usr/bin/env bash

source experiment_manager/infra/.env

git remote add gitlab "http://root:$GITLAB_ROOT_PASSWORD@$GITLAB_HOSTNAME:$GITLAB_PORT/$GITLAB_THIS_PROJECTNAME"
git push gitlab main
