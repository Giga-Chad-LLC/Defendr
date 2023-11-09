.PHONY: run-prod
run-prod:
	uvicorn server.server:app --host 0.0.0.0

.PHONY: run
run:
	uvicorn server.server:app --reload --port 8347

.PHONY: server
server:
	python -m server.server

.PHONY server-detached
server-detached:
	nohup make server &
