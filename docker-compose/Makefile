start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

# Technical indicators pipeline management
build-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml build

start-technical-indicators-pipeline: build-technical-indicators-pipeline
	docker compose -f technical-indicators-pipeline.yml up -d

stop-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml down