dependencies:
	sudo apt-get -qq update
	apt-get install -y  python-pypy.sandbox
	pip install flake8

test:
	pypy-sandbox --tmp=. --timeout=10 ./tsampi/test_validator.py

pep8:
	flake8 */*.py --ignore E402,E501
