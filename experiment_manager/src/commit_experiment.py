#!/usr/bin/env python3

import git
import pathlib
import shutil
import sys
import os
from secrets import token_hex


def getMainDir():
    return pathlib.Path(__file__).parent.parent.parent.absolute()

def gitRecoveryWrapper(func):
    '''Recovers git HEAD and index state.'''
    def wrap(*args, **kwargs):
        dirPath = getMainDir()
        os.makedirs(f'{dirPath}/tmp', exist_ok=True)
        shutil.copy(f'{dirPath}/.git/index', f'{dirPath}/tmp/index')
        returns = func(*args, **kwargs)
        shutil.move(f'{dirPath}/tmp/index', f'{dirPath}/.git/index')
        return returns
    return wrap


def getRepo() -> git.Repo:
    dirPath = getMainDir()
    return git.Repo(dirPath)


@gitRecoveryWrapper
def commit(file_to_execute) -> str:
    '''Commits all changes to an experiment's commit.'''
    repo = getRepo()
    original_branch = repo.active_branch
    experiment_branch = repo.create_head(f'experiment-{token_hex(16)}')

    repo.git.checkout(experiment_branch)

    repo.git.add(update=True)
    repo.index.commit(str(file_to_execute))
    repo.git.push('gitlab', experiment_branch)

    repo.git.checkout(original_branch)


if __name__ == '__main__':
    commit(sys.argv[1])
