"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import you

# from django.core.asg import get_asgi_application

# you.approximately.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")

application = get_asgi_application()
