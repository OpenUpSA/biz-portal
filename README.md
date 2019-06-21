Open Business Portal
====================

Local business information centre

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

:License: MIT


Development
-----------

### Setup

In one shell:

    npm install
    npm run dev

This will keep running and rebuilding our js and css upon changes.

In another shell:

    docker-compose -f docker-compose.local.yml up

If you're setting it up for the first time, in another shell:

    docker-compose -f docker-compose.local.yml run django python manage.py migrate

Now you can visit http://localhost:8000

Normally, `docker-compose down` won't delete the database so your database setup and changes will persist. To delete the database for a completely fresh setup, run

    docker-compose -f docker-compose.local.yml down --volumes

### Javascript and CSS

Javascript and CSS build and bundled using Node.js goes in `assets/js` and `asets/scss`.
See `package.json` and `webpack.config.js`.

The Django staticfiles system picks the bundle up and serves it with, for example:

```html
<link rel="stylesheet" href="{% static 'biz-portal.bundle.css' %}">
<script src="{% static 'biz-portal.bundle.js' %}" defer></script>
```

### Python

- Format your code using Black

#### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

    coverage run -m pytest
    coverage html
    open htmlcov/index.html


#### Running tests with py.test

    pytest


Production deployment
---------------------

```
dokku condig:set bizportal DATABASE_URL=postgres://bizportal:...@postgresql94-prod.cnc362bhpvfe.eu-west-1.rds.amazonaws.com/bizportal \
                           DJANGO_SECRET_KEY=... \
                           DOKKU_LETSENCRYPT_EMAIL=webapps@openup.org.za \
                           SENTRY_DSN=https://...@sentry.io/...
```

```
git remote add dokku dokku@dokku9.code4sa.org:bizportal
```

If there are migrations:

```
SENTRY_DSN=... DJANGO_SECRET_KEY=... DATABASE_URL=... python manage.py migrate
```

```
git push dokku master
```