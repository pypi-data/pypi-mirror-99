=====
api
=====

Django-authapi is a app that provide all urls four your authentication in your backend api.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "api" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'api',
    ]

2. Include the api URLconf in your project urls.py like this::

    path('api/', include('api.urls')),

4. Run `python manage.py makemigrations api` to make migrations for this app .


3. Run `python manage.py migrate` to create the api models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to see docs (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/ to participate all urls related to authentication backend api.