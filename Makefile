PHONY: deps

all: deps
	PYTHONPATH=.venv ; . .venv/bin/activate

.venv:
	if [ ! -e ".venv/bin/activate.py" ] ; then pyvenv --clear --without-pip .venv ; fi

deps: .venv requirements.txt dev_requirements.txt _test_requirements.txt
	PYTHONPATH=.venv ; . .venv/bin/activate && curl https://bootstrap.pypa.io/get-pip.py | python && .venv/bin/pip install -r full_requirements.txt && .venv/bin/pip install -e .

test: .venv setup.py
	PYTHONPATH=.venv ; . .venv/bin/python setup.py test

clean:
	rm -rf .venv build *.egg-info
	rm -f `find . -name \*.pyc -print0 | xargs -0`
