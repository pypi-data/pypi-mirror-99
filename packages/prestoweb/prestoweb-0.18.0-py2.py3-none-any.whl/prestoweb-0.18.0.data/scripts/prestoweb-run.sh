#!/usr/bin/env bash

export SECRET_KEY=1234
export SQLITE3_DIR=${HOME}/prestoweb_data

uwsgi --http-socket 0.0.0.0:8001 \
    --master \
    --workers 1 \
    --module prestoweb.prestoweb.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=prestoweb.prestoweb.settings \
    --vacuum \
    --die-on-term
