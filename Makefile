.PHONY: build up down logs clean restart

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf chroma_db/*
	find . -type d -name "__pycache__" -exec rm -r {} +

restart:
	docker-compose down
	docker-compose up -d

setup:
	cp .env.example .env
	mkdir -p chroma_db
	chmod 666 documents.db || true
	chmod -R 777 chroma_db || true 