########################################
## Redpanda management
########################################

start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1

########################################
## Technical indicators pipeline 
########################################

# for live data
build-technical-indicators-live:
	docker compose -f technical-indicators-live.yml build

start-technical-indicators-pipeline: build-technical-indicators-live
	docker compose -f technical-indicators-live.yml up -d

stop-technical-indicators-pipeline:
	docker compose -f technical-indicators-live.yml down

# Technical indicators pipeline management
# for historical data
build-technical-indicators-historical:
	docker compose -f technical-indicators-historical.yml build
	
backfill-technical-indicators: build-technical-indicators-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f technical-indicators-historical.yml up -d

########################################
## News signal pipeline 
########################################

# For live
build-news-signal-live:
	docker compose -f news-signal-live.yml build

start-news-signal-live: build-news-signal-live
	docker compose -f news-signal-live.yml up -d

stop-news-signal-live:
	docker compose -f news-signal-live.yml down

# for historical data
build-news-signal-historical:
	docker compose -f news-signal-historical.yml build

backfill-news-signals: build-news-signal-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill of news signals with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f news-signal-historical.yml up -d

########################################
## Clean up
########################################

clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*historical.*"
