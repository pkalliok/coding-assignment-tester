
try: stamps/reqs stamps/db
	./myenv/bin/python manage.py runserver

shell: stamps/reqs stamps/db
	./myenv/bin/python manage.py shell

myenv:
	python3 -m venv myenv

tags:
	ctags -R tester

stamps/reqs: requirements.txt myenv
	./myenv/bin/pip install -r requirements.txt
	touch $@

stamps/db: stamps/models myenv
	./myenv/bin/python manage.py migrate
	touch $@

stamps/models: tester/models.py myenv
	./myenv/bin/python manage.py makemigrations tester
	touch $@

