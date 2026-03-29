.PHONY: dev api frontend install train build

dev:
	@echo "Starting API and frontend..."
	$(MAKE) -j2 api frontend

api:
	uvicorn backend.api:app --host 0.0.0.0 --port 8080 --reload

frontend:
	cd frontend && npm run dev

install:
	pip install -r requirements.txt
	cd frontend && npm install

train:
	python -m generator
	python -m backend.train

build:
	cd frontend && npm run build
