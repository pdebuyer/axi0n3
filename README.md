# axione

# Docker build

You can use docker to build your app.

```
docker build . -t axione_api
```

and then use docker compose.

```
docker compose up
```

Sometimes, you need to create a folder db-data in root folder to be able to start the docker.
This folder is needed for the postgres database.

# API usage

Send a get requests with the following arguments : 
- departement
- max_loyer
- surface

departement is the number of the department and must have at least 2 characters (1 -> 01).


You can use {host}/docs to view the fastapi docs
