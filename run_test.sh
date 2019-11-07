#!/usr/bin/env bash
docker-compose up -d --build
docker-compose run web python manage.py test
