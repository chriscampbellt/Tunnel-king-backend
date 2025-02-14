# /bin/bash
cr:
	docker compose -f docker-compose.cr.yml up --build

dev.build:
	docker compose -f docker-compose.dev.yml build

dev.makemigrations:
	docker compose -f docker-compose.dev.yml exec django python manage.py makemigrations

dev.migrate:
	docker compose -f docker-compose.dev.yml exec django python manage.py migrate

dev.admin_generator:
	docker compose -f docker-compose.dev.yml exec django python manage.py admin_generator $(APP)

dev.startapp:
	docker compose -f docker-compose.dev.yml exec django sh -c "cd apps && python ../manage.py startapp $(APP)"

dev.up.d:
	docker compose -f docker-compose.dev.yml up -d

dev.up:
	docker compose -f docker-compose.dev.yml up

dev.down:
	docker compose -f docker-compose.dev.yml down

dev.dcshell:
	docker compose -f docker-compose.dev.yml exec django /bin/bash

dev.collectstatic:
	docker compose -f docker-compose.dev.yml exec django python manage.py collectstatic

dev.msshell:
	docker compose -f docker-compose.dev.yml exec model_server /bin/bash

dev.ollama_shell:
	docker compose -f docker-compose.dev.yml exec ollama /bin/bash
