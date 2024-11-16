import os

from celery import Celery  # type:ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "My_Shop.settings")
app = Celery("My_Shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_url = "amqp://guest:guest@localhost"
