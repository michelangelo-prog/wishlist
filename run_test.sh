#!/usr/bin/env bash
docker-compose up -d --build
docker-compose run web python manage.py test
docker-compose run web flake8 web
