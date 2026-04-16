from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "legal_rag",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=["app.workers.ingestion_worker"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_queues={
        "ingestion_queue": {},
        "query_queue": {},
    },
    task_default_queue="ingestion_queue",
)