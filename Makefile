src = textube.py ytapi.py test/test_ytapi.py

all: check

test:
	python -m unittest -v test.test_ytapi

init:
	python -m pip install -r requirements.txt

check:
	pyflakes $(src)

shell: .venv
	pipenv shell

gvim:
	gvim -o $(src)
