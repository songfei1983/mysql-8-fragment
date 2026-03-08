.PHONY: help up down install init fragment fragment-once defrag status clean

PYTHON := python
DOCKER_COMPOSE := docker-compose

help:
	@echo "Available commands:"
	@echo "  make up            - Start MySQL container"
	@echo "  make down          - Stop MySQL container"
	@echo "  make install       - Install Python dependencies"
	@echo "  make init          - Initialize data (inserts ~40M rows, takes time)"
	@echo "  make fragment      - Run fragmentation cycle until >1GB free space"
	@echo "  make fragment-once - Run a single fragmentation cycle"
	@echo "  make defrag        - Run online DDL to reclaim space"
	@echo "  make status        - Check table size and fragmentation"
	@echo "  make clean         - Stop container and remove volumes (RESET DB)"

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

install:
	pip install mysql-connector-python

init:
	$(PYTHON) insert_composite_key_table.py

fragment:
	$(PYTHON) run_fragment_until.py

fragment-once:
	$(PYTHON) fragment_test.py

defrag:
	$(PYTHON) alter_test.py

status:
	$(PYTHON) query_table_size.py

clean:
	$(DOCKER_COMPOSE) down -v
