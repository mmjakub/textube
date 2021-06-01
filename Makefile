main = textube
src = $(main).py test_$(main).py

all: check

test: test_$(main).py
	python -m unittest -v test_$(main)

test.%:
	python -m unittest -v test_$(main).$*

init:
	python -m pip install -r requirements.txt

check:
	pyflakes $(src)

shell: .venv
	pipenv shell

gvim:
	gvim -o $(src)
