from celery import Celery

from app.config import settings


celery_app: Celery = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['app.tasks.tasks']
)
