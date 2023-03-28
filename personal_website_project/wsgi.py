"""
WSGI config for personal_website_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
path = '/personal_website_project'
if path not in sys.path:
    sys.path.append(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_website_project.settings')

application = get_wsgi_application()
