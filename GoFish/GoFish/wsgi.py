"""
WSGI config for GoFish project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

# TURN ON THE VIRTUAL ENVIRONMENT FOR YOUR APPLICATION
activate_this = '/home/lapinas/.virtualenvs/gofish/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import os
import sys

# ADD YOUR PROJECT TO THE PYTHONPATH FOR THE PYTHON INSTANCE
path = 'home/lapinas/Go-Fish/GoFish'
if path not in sys.path:
    sys.path.append(path)

# IMPORTANTLY GO TO THE PROJECT DIR
os.chdir(path)

# TELL DJANGO WHERE YOUR SETTINGS MODULE IS LOCATED
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoFish.settings')

# IMPORT THE DJANGO SETUP - NEW TO 1.7
import django
django.setup()

# IMPORT THE DJANGO WSGI HANDLER TO TAKE CARE OF REQUESTS
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()