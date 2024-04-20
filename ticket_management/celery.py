import os

from dotenv import dotenv_values
get_env_var = dotenv_values()

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_management.settings')

app = Celery(get_env_var['SERVER_APP'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.result_backend = 'celery.backends.logging.LoggingResultBackend'

app.conf.worker_concurrency = int(get_env_var['WORKER_CONCURRENCY'])
app.conf.worker_prefetch_multiplier = int(get_env_var['WORKER_PREFETCH_MULTIPLIER'])
app.conf.worker_max_tasks_per_child = int(get_env_var['WORKER_MAX_TASKS_PER_CHILD'])

app.conf.worker_max_memory_per_child = int(get_env_var['MAX_MEMORY_PER_CHILD'])
app.conf.worker_max_memory_per_worker = int(get_env_var['MAX_MEMORY_PER_WORKER'])

app.conf.broker_connection_retry_on_startup = get_env_var['CONNECTION_RETRY_STARTUP']

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
