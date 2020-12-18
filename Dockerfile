# ==============================
FROM helsinkitest/python:3.7-slim as appbase
# ==============================

ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN mkdir /entrypoint

COPY --chown=appuser:appuser requirements*.txt /app/

RUN apt-install.sh \
    build-essential \
    libpq-dev \
    netcat \
    && pip install --no-cache-dir \
    -r /app/requirements.txt \
    && pip install --no-cache-dir \
    -r /app/requirements-prod.txt \
    && apt-cleanup.sh \
    build-essential \
    pkg-config

COPY --chown=appuser:appuser docker-entrypoint.sh /entrypoint/
ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]

# ==============================
FROM appbase as staticbuilder
# ==============================

ENV VAR_ROOT /app
COPY --chown=appuser:appuser . /app
RUN python manage.py collectstatic --noinput

# ==============================
FROM appbase as production
# ==============================

ENV VAR_ROOT /app
COPY --from=staticbuilder --chown=appuser:appuser /app/static /app/static
COPY --chown=appuser:appuser . /app/

USER appuser

EXPOSE 8000/tcp

