.PHONY: install run test lint format clean

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	python -m pytest tests/ -v

lint:
	flake8 app/

format:
	black app/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +