"""
ASGI config for moviestore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/'



 Django, being a web framework, needs a web server to operate. And since most web servers don’t natively speak Python, we need an interface to make that communication happen. Django currently supports two interfaces – Web Server Gateway Interface (WSGI) and Asynchronous Server Gateway Interface (ASGI). The asgi.py file contains an entry point for ASGI-compatible web servers to serve your project asynchronously.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviestore.settings')

application = get_asgi_application()
