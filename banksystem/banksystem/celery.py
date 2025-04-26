import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksystem.settings')

app = Celery('banksystem')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
