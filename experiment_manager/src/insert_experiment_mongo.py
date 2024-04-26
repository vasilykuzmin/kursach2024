#!/usr/bin/env python3

import pymongo
import sys
import pathlib
import os
from dotenv import load_dotenv
import json


def insertExperimentInMongo(path):
    load_dotenv(dotenv_path=f'{pathlib.Path(__file__).parent.parent}/infra/.env')

    client = pymongo.MongoClient(f"mongodb://{os.environ['MONGO_ROOT_USER']}:{os.environ['MONGO_ROOT_PASSWORD']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}/")
    experiments = client.experiments.experiments

    with open(path, 'r') as f:
        experiment = json.load(f)

    experiments.insert_one(experiment)


if __name__ == '__main__':
    insertExperimentInMongo(sys.argv[1])
