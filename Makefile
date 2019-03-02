run.server:
	docker run --name=server -ti --rm -p 8080:8080 gdtb:latest wapi.py --start-server

run.reactor:
	docker run --name=reactor -ti --rm gdtb:latest wapi.py --start-reactor

run.database:
	docker run --name=postgres -ti --rm -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres:latest

build:
	docker build --no-cache -t gdtb:latest .