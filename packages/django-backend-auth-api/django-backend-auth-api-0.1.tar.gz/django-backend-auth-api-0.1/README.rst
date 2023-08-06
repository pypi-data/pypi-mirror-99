================
BACKEND-AUTH-API
================

BACKEND-AUTH-API is a app to manage your authentication backend api with integrated doc.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "apiauth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'apiauth',
    ]

2. Include the apiauth URLconf in your project urls.py like this::

    path('apiauth/', include('apiauth.urls')),

4. Run `python manage.py makemigrations apiauth` to make migrations for this app .


3. Run `python manage.py migrate` to create the apiauth models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to see docs (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/apiauth/ to participate all urls related to authentication backend apiauth.