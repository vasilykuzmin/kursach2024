#!/usr/bin/env python3

import pathlib
import subprocess
import sys

def getMainDir():
    return pathlib.Path(__file__).parent.parent.parent.absolute()

def run(file):
    bashCommand = f'jupyter nbconvert --to python --execute {getMainDir() / file}'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    print(f'Output: {output}')

    if error is not None:
        print(f'Error: {error}')
        return


if __name__ == '__main__':
    run(sys.argv[1])
