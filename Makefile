src = textube/textube.py textube/ytapi.py tests/test_ytapi.py

all: check

test:
	python -m unittest tests.test_ytapi

init:
	python -m pip install -r requirements.txt

check:
	pyflakes $(src)

shell: .venv
	pipenv shell

gvim:
	gvim -o $(src)

.PHONY: all test init check shell gvim
