================================
Reaktion's CRM plugin for Django
================================

Reaktion CMS is a Django app is simple CRM connected to tracking system.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add ``django_reaktion_crm`` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-reaktion-crm',
    ]


2. To create the polls models run::

    python manage.py migrate


3. Set up ``MONGO_CONN`` and ``DOMAIN_ID`` env

4. Import contacts from .csv file ::

    python manage.py import_csv filename <filename>

5. Import tracking ::

    python manage.py import_tracking delta <hours>

