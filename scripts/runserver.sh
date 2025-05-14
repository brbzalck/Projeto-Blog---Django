#!/bin/sh

gunicorn djangoapp.wsgi:application --bind 0.0.0.0:8000