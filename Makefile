up:
	docker compose up -d

down:
	docker compose down

gen:
	python src/generate_source_data.py

etl:
	python src/etl.py

dq:
	python src/run_quality_checks.py

all: up gen etl dq
