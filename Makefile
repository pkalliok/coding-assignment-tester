
try: stamps/reqs stamps/db
	./myenv/bin/python manage.py runserver

shell: stamps/reqs stamps/db
	./myenv/bin/python manage.py shell

myenv:
	python3 -m venv myenv

stamps/reqs: requirements.txt
	./myenv/bin/pip install -r requirements.txt
	touch $@

stamps/db: stamps/models
	./myenv/bin/python manage.py migrate
	touch $@

stamps/models: tester/models.py
	./myenv/bin/python manage.py makemigrations tester
	touch $@

