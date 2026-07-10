from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery = Celery(
    "dlas",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery.autodiscover_tasks(
    packages=["worker"]
)