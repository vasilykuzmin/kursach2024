#!/usr/bin/env python3

import git
import pathlib
import shutil
import sys
import os
from secrets import token_hex


def getMainDir():
    return pathlib.Path(__file__).parent.parent.parent.absolute()


def getRepo() -> git.Repo:
    dirPath = getMainDir()
    return git.Repo(dirPath)


def commit(file_to_execute) -> str:
    '''Commits all changes to an experiment's commit.'''
    experiment_name = f'experiment-{token_hex(16)}'

    repo = getRepo()
    original_branch = repo.active_branch

    repo.git.stash(experiment_name)

    experiment_branch = repo.create_head(experiment_name)
    repo.git.checkout(experiment_branch)

    repo.git.stash.apply(experiment_name)
    repo.git.add(update=True)
    repo.index.commit(str(file_to_execute))
    repo.git.push('gitlab', experiment_branch)

    repo.git.checkout(original_branch)
    repo.git.stash.pop(experiment_name)

if __name__ == '__main__':
    commit(sys.argv[1])
