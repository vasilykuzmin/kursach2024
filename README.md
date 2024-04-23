# Setup
* Install docker and docker-compose
* Go to experiment_manager/infra and run `docker-compose up`
* Check gitlab host and port and root password in `experiment_manager/inrfa/.env` file
* Go to gitlab web ui and create runner authorization token.
* Run `register_runner.sh <token>`