#!/bin/bash

set -e

if [ -z "$SKIP_DATABASE_CHECK" -o "$SKIP_DATABASE_CHECK" = "0" ]; then
    until nc -z -v -w30 "$DATABASE_HOST" 5432
    do
      echo "Waiting for postgres database connection..."
      sleep 1
    done
    echo "Database is up!"
fi


# Apply database migrations
if [[ "$APPLY_MIGRATIONS" = "1" ]]; then
    echo "Applying database migrations..."
    ./manage.py migrate --noinput
fi

# Create superuser
if test -z "$DONT_CREATE_SUPERUSER"; then
    if test -z "$ADMIN_USER_PASSWORD"; then
	ADMIN_USER_PASSWORD="$(dd if=/dev/urandom bs=32 count=1 | base64)"
    fi
    DJANGO_SUPERUSER_PASSWORD="$ADMIN_USER_PASSWORD" \
	    ./manage.py createsuperuser --username admin \
	    --noinput --email admin@example.com && \
    echo "Admin user created with credentials admin:$ADMIN_USER_PASSWORD (email: admin@example.com)"
fi

# Start server
if [[ ! -z "$@" ]]; then
    "$@"
elif [[ "$DEV_SERVER" = "1" ]]; then
    python ./manage.py runserver 0.0.0.0:8000
else
    uwsgi --ini .prod/uwsgi.ini
fi
