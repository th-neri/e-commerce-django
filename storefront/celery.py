import os
from celery import Celery

# setting DJANGO_SETTINGS_MODULE to the storefront settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

celery = Celery('storefront')
celery.config_from_object('django.conf:settings', namespace='CELERY') # to specify where celery can find configuration variables
celery.autodiscover_tasks() # to instruct celery to automatically discover the tasks