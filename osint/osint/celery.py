from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'osint.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('osint')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "get_random_joke": {
#         "task": "view_block.tasks.get_random_joke",
#         "schedule": 15.0,
#     }
# }

@app.task(bind=True)
def debug_task(self):
       print('Request: {0!r}'.format(self.request))