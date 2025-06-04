import os

from celery import Celery

from config.settings import base as settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

app = Celery("config")
app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

BROKER_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"  # noqa

app.conf.update(
    broker_url=BROKER_URL,
    result_backend=BROKER_URL,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    task_always_eager=not BROKER_URL,
    timezone="Asia/Tashkent",
)
