.PHONY: run-prod
run-prod:
	uvicorn server.server:app --host 0.0.0.0

.PHONY: run
run:
	uvicorn server.server:app --reload