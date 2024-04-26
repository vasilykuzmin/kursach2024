# Setup
* Install docker and docker-compose
* Go to experiment_manager/infra and run `docker-compose up`
* Check gitlab host and port and root password in `experiment_manager/inrfa/.env` file
* Go to gitlab web ui and create runner authorization token.
* Run `register_runner.sh <token>`
* Run `register_repo.sh` to add this repo to gitlab.
* (Optional) Install `seunlanlege.action-buttons` vs code extension.

# Run
* `pip3 -m venv ./.venv`
* `source ./.venv/bin/activate`
* Run model locally
* Run model remotely with commit button in left bottom side of vs code or `experiment_manager/src/commit_experiment.py path/to/your/file.ipynb`
