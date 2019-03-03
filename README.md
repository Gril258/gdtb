# GDT Backend for Bands

- reactor.py - main program that do corutines to get data and authenticate bands
- wapi.py - web based api for managing bands and users

## INSTALL

Requirements:

- python 3.6
- docker (optional)
- glib2-devel (bluepy)
- python modules: flask, asyncio, aiopg, psycopg2-binary, pycrypto, bluepy

To make virtualenv:

```
$ python3 -m venv env/
$ . env/bin/activate
$ pip install -r requirements.txt
$ python wapy.py
```

To run docker containers:

```
$ docker-compose up -d --build
$ docker logs server
$ docker logs reactor
$ docker logs postgres
```

To stop docker containers:

```
$ docker-compose down
```