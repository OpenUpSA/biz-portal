Open Business Portal
====================

Local business information centre

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

:License: MIT


Development
-----------

### Setup

    docker-compose -f docker-compose.local.yml up

If you're setting it up for the first time, in another shell:

    docker-compose -f docker-compose.local.yml run django python manage.py migrate

Now you can visit http://localhost:8000

Normally, `docker-compose down` won't delete the database so your database setup and changes will persist. To delete the database for a completely fresh setup, run

    docker-compose -f docker-compose.local.yml down --volumes

### Python

- Format your code using Black

#### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

    coverage run -m pytest
    coverage html
    open htmlcov/index.html


#### Running tests with py.test

    pytest
