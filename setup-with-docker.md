# Docker Setup

Use this guide if you want to use Docker in your project.

> Built with Docker v18.03.1-ce.

## Getting Started

Update the environment variables in *docker-compose.yml*, and then build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

By default the app is set to use the production configuration. If you would like to use the development configuration, you can alter the `APP_SETTINGS` environment variable:

```
APP_SETTINGS="web.domain.config.DevelopmentConfig"
```

Create the database:
-
```sh
$ docker-compose run web python manage.py db upgrade
```

Access the application at the address [http://localhost:5002/](http://localhost:5002/)

### Run tests

```sh
docker-compose run web python manage.py test-pytest
```

### Run tests with black, isort and flakes

```sh
docker-compose run web python manage.py test-pytest-with-plugins
```
