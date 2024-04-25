# Cyrus: Xeneta Ocean Rates API Service

This Flask API provides average shipping rates for specified routes over given date ranges, utilizing a PostgreSQL database to execute queries and return JSON formatted data.

## Project Structure
- `app/`: Flask application.
  - `__init__.py`: Initializes the app and imports routes.
  - `database.py`: Manages database connections .
  - `routes.py`: Defines API endpoints and queries.
- `tests/`: Contains test cases.
  - `tests.py`: Main test script.
- `requirements.txt`: Lists the dependencies.
- `run.py`: Script to run the Flask server.
- `docker/`: Contains dockerfile setup and rates data.

# Launching the Docker Container

## Building the Container
The goal is to run the database in the docker container and access it from the host machine.
First, build the Docker container for the application using the provided Dockerfile:

```bash
sudo docker build -f Dockerfile -t xeneta-container .
```

## Running the Container

To run the image as a container, use:

```bash
sudo docker run -d --name xeneta-rates -p 5432:5432 xeneta-container
```
This command starts a container named xeneta-rates in detached mode and maps port 5432 on the host to port 5432 in the container.


## Logging in to PostgreSQL
With the container running, you can login to the PostgreSQL database:

```bash
psql -h localhost -p 5432 -U postgres -d postgres
```
When prompted, enter the password: `ratestask`.

## Exploring the Database
Within the PostgreSQL interface, use the following commands to explore the database:

List all tables:

`\dt
`

Select all records from the region table for instance:

`SELECT * FROM regions;
`

## Flask app Installation and Setup

Ensure Python 3 and PostgreSQL are installed.

Clone the repository: 


Create and activate the virtual environment:
`python -m venv .venv`

activate it

`source .venv/bin/activate # On Windows, use .venv\Scripts\activate`


Install dependencies:
`pip install -r requirements.txt`

Configure your database in `database.py` with the appropriate credentials.

## Running the Application

To start the application, run:
`flask run`


The server will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints

### Retrieve Rates

`GET /rates`

**Parameters:**
- `date_from`: Start date (YYYY-MM-DD).
- `date_to`: End date (YYYY-MM-DD).
- `origin`: Origin location code or slug.
- `destination`: Destination location code or slug.

**Sample URLs:**

- Daily average rates with slugs and codes:
  `http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main`
  
- Daily rates using slugs:
  `http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-08&origin=china_south_main&destination=north_europe_main`
  
- Daily rates using codes:
  `http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-05&origin=CNGGZ&destination=EETLL`

## Testing

Run tests with:
`python -m unittest tests/tests.py`


## Built With

- [Flask](http://flask.palletsprojects.com/) - The web framework used.
- [psycopg2](https://www.psycopg.org/) - PostgreSQL adapter for Python.

## Authors

- **Cyrus Jomo** 




