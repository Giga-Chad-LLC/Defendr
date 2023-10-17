# Defendr
---

## Participants:

1. Vladislav Artiukhov (vartiukhov@constructor.university)
2. Vladislav Naumkin (vnaumkin@constructor.university)

## Deploy

Here is the hosted website of the homework 4 on **GitHub Pages**: https://giga-chad-llc.github.io/Defendr/



## Configuration:

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