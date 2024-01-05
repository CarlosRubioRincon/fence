# fence

## REST API built with FastAPI and Postgres

This is a example of a REST API built with FastAPI and Postgres running on Docker.

The DB consists of a single table named `country` that is seeded during the startup process.

The API exposes the following the following resources and operations:

#### Get the list of countries

`curl --location --request GET 'http://0.0.0.0:8000/countries'`

#### Get a country by ID

`curl --location --request GET 'http://0.0.0.0:8000/country/{country_id}'`

#### Get a country by country code

`curl --location --request GET 'http://0.0.0.0:8000/country/?country_code={country_code}'`

#### Create a country

```
curl --location 'http://0.0.0.0:8000/country' \
--header 'Content-Type: application/json' \
--data '{
    "name":"Spain",
    "code": "ES"
}'
```

#### Delete a country

```
curl --location --request DELETE 'http://0.0.0.0:8000/country/{country_id}'
```


## How to run

You need Docker and Docker Compose installed in your local machine.

In order to spin up the infrastructure:

`docker-compose up --build -d`

In order to tear down the infrastructure:

`docker-compose down --volumes`

## Design comments

* API designed following a simple approach with 3 layers (API, domain, DB)
* Testing is missing, for the sake of this example, I've manually tested the endpoints
* Code hasn't been linted