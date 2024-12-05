run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t trades .

build-multistage:
	docker build -f multistage.Dockerfile -t trades:multistage .