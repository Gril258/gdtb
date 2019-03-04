# GDT Backend for Bands

- reactor.py - main program that do corutines to get data and authenticate bands
- wapi.py - web based api for managing bands and users

## Requirements:

- Linux
- python 3.6+
- docker (optional)
- glib2-devel (bluepy)
- python modules: flask, asyncio, aiopg, psycopg2-binary, pycrypto, bluepy

## To make python3 virtualenv:

```
$ python3 -m venv env/
$ . env/bin/activate
$ pip install -r requirements.txt
$ python wapi.py --start-server
$ python wapi.py --start-reactor
```

## To run docker containers:

```
$ docker-compose up -d --build
$ docker-compose ps
$ docker-compose logs server
$ docker-compose logs reactor
$ docker-compose logs postgres
```

## To stop docker containers:

```
$ docker-compose down
```