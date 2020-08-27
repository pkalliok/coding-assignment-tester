
myenv:
	python3 -m venv myenv

stamps/reqs: requirements.txt
	./myenv/bin/pip install -r requirements.txt
	touch $@
