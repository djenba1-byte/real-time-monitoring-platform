.PHONY: up down logs test e2e-demo webhook-test

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	python -m pytest -q

e2e-demo:
	./scripts/trigger_e2e_demo.sh

webhook-test:
	./scripts/send_direct_webhook_test.sh
