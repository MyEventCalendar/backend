#! /usr/bin/env bash

python3 /app/src/manage.py migrate
python3 /app/src/manage.py runserver
