## This is a flask server that implements [Clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html "Clean architecture") using Python.

### Features demonstrated:

**1.A minimal scalable flask server:**

- [ ] **Clean Architecture** with replaceable components (e.g Database types and other "external systems")
- [ ] Automated **Unit tests** for models and endpoints
- [ ] Automated **Integration test**
- [ ] Automated **Test coverage**
- [ ] **Containerised** Postgres database
- [ ] Containerised Flask server
- [ ] Deployed Flask using **Gunicorn** production server
- [ ] Containerised **Nginx reverse proxy**
- [ ] **Automated migration** during deployment steps using **Alembic**
- [ ] **Request validation**
- [ ] Using [Media Group API](https://github.com/M-Media-Group/Covid-19-API).

### Overview:

- The data loaded from  [Media Group API](https://github.com/M-Media-Group/Covid-19-API) is filtered and formated to match the DB models used in order to demonstrate ent to end Architecture design.
  i.e flat DB models is used
- Authorization and authentication is assumed out of scope due to limited time

## Requirements & Tools used.

- [ ] Docker installed in the target system
- [ ] Anaconda python is used for the readily available packages
- [ ] Python 3.9.12
- [ ] conda version ```4.13.0```
- [ ] M1 (Apple Silicon) OS environment in case you need to resolve compatibility of tools installed. Something may vary.
- [ ] All packages used are latest stable versions.

## Setup Procedure

### CD into the project and install requirements (See the requirements' folder)

```shell
 $ pip install -r requirements/test.txt
 $ pip install -r requirements/dev.txt
 $ pip install -r requirements/prod.txt
```

### Run tests:

```shell
$ python3 manage.py test -- --integration
```

> This tests the entire setup process including containerization, executes all available unit and integration tests and reports coverage.

### Build the server container image:

```shell
$ python3 manage.py compose build web
```

### Start the containers:

```shell
$ python3 manage.py compose up -d
```

### Initialise Postgres database:

```shell
$ python3 manage.py init-postgres
```

### Use the following command to run PostgreSQL with the user ```postgres``` to explore DB status at this point:

```shell
$ python3 manage.py compose exec db psql -U postgres
```

### Use the following command to check available database:

```shell
$ postgres=# \l
```

### Use the following command to connect with the application database:

```shell
$ postgres=# \c application
```

### Use the following command to check available tables/relations in the application database:

```shell
$ application=# \dt
 ```

### Initialize migrations Alembic (Create tables and manage DB versions):

```shell
$ alembic init migrations
```

### Autogenerate database versions:

```shell
$ POSTGRES_USER=postgres\
  POSTGRES_PASSWORD=postgres\
  POSTGRES_HOSTNAME=localhost\
  APPLICATION_DB=application\
  alembic revision --autogenerate -m "Initial"
```

### Apply migrations:

```shell
$ POSTGRES_USER=postgres\
  POSTGRES_PASSWORD=postgres\
  POSTGRES_HOSTNAME=localhost\
  APPLICATION_DB=application\
  alembic upgrade head
```

## API test and explanation:

- Server runs you on ```http://0.0.0.0:8000```
- Make any request to ```http://0.0.0.0:8000/covidcases/listcases``` will trigger loading of data from [Media Group API](https://github.com/M-Media-Group/Covid-19-API) of not loaded already.

## Sample requests (See test cases' samples):

```http request
### GET Get list of covid cases in countries
GET http://localhost:8080/covidcases/listcases
Accept: application/json

### Sample filter
GET http://localhost:8080/covidcases/listcases?confirmed__gt=2604594&confirmed__lt=2604596
Accept: application/json


### Add case
POST http://localhost:8080/covidcases/savecases
Content-Type: application/json

{
  "confirmed": 2604595,
  "recovered": 195365,
  "deaths": 62548,
  "country": "MyCountry",
  "population": 64979548,
  "sq_km_area": 551500,
  "life_expectancy": "78.8",
  "elevation_in_meters": 375,
  "continent": "Europe",
  "abbreviation": "FR",
  "location": "Western Europe",
  "capital_city": "Paris",
  "lat": "46.2276",
  "long": "2.2137",
  "updated": "2020/12/26 12:21:56+00"
}

```

# Coming up:

> Minimal React.js analytics dashboard for the API