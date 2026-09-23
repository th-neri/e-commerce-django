"""
ASGI config for storefront project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

# if running on render, load the production file otherwise, load development
if os.getenv('RENDER'):
    load_dotenv('.env.prod')
else:
    load_dotenv('.env.dev')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

application = get_asgi_application()
