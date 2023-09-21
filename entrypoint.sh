#!/bin/sh

gunicorn -c gunicorn_config.py backend.wsgi:application
