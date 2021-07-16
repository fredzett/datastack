#.ONESHELL:

#env:#
#	conda activate datastack

# tests/test_datatable.py
#tests/test*.py    
entr:
	ls */*.py | entr -c pytest -v tests/test_*.py

test:
	pytest tests/test_datatable.py

clean:
	rm -rf tests/__pycache__ .pytest_cache

black: 
	black datastack/*.py

flake:
	flake8 datastack/datacolumn.py

check: test clean flake

run: test clean black