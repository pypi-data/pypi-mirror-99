================
BACKEND-AUTH-API
================

BACKEND-AUTH-API is a app to manage your authentication backend api with integrated doc.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "authapi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'authapi',
    ]

2. Include the authapi URLconf in your project urls.py like this::

    path('authapi/', include('authapi.urls')),

4. Run `python manage.py makemigrations authapi` to make migrations for this app .


3. Run `python manage.py migrate` to create the authapi models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to see docs (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/authapi/ to participate all urls related to authentication backend apiauth.