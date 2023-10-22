# Defendr
---

## Participants:

1. Vladislav Artiukhov (vartiukhov@constructor.university)
2. Vladislav Naumkin (vnaumkin@constructor.university)

## Deploy

Here is the hosted website of the **homework 4** on **GitHub Pages**: https://giga-chad-llc.github.io/Defendr/


## Demo

![Assignment 5 | Use case](./src/assets/videos/assignment-5-use-case.gif)


## Configuration:

First, install all dependancies via:
```bash
pip install -r ./requirements.txt
```

To start the server run `make run` or `make run-prod` (see [`Makefile`](Makefile)), that will start the server on `localhost:8000`:
```bash
uvicorn server.server:app --reload
```

In order to connect to the database adjust the [`server/.env`](server/.env) file to match the database parameters, e.g.:
```bash
# These params configured to match the database instance created via 'docker-compose.yaml'
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123
DB_DATABASE=defendr
```

Open `index.html` and navigate to the dashboard panel to see the dashboard; insert some data and press the sumbit button.

---

There is a `docker/docker-compose.yaml` file with **MySQL** and **Adminer** services. To start the services navigate to the root folder of the project and run the following:
```bash
docker-compose -f ./docker/docker-compose.yaml up
```

To populate the database with fake data use the script `scripts/python/populate_data.py`, it order to execute the script run the following from the root directory:
```bash
# insure that the dependancies mentioned in 'requirements.txt' are satisfied
# (i.e. run `pip install -r ./requirements.txt`)
python -m scripts.python.populate_data
```