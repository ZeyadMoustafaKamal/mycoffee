#!/bin/sh

gunicorn -c gunicorn.config.py backend.wsgi:application
