#.ONESHELL:

#env:#
#	conda activate datastack
entr:
	ls datastack/datatable.py | entr -c pytest -v tests/test_datatable.py    

test:
	pytest tests/test_datatable.py

clean:
	rm -rf tests/__pycache__ .pytest_cache

black: 
	black datastack/*.py

flake:
	flake8 datastack/datatable.py

check: test clean flake
