import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InstaGpt.settings")

app = Celery('InstaGpt',include=['InstaGpt.task'])
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = 'Asia/Kolkata'


if __name__ == '__main__':
    app.start()
