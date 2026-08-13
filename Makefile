install:
	python -m pip install -r requirements.txt
run:
	uvicorn app.api.main:app --reload
 test:
	pytest -q
