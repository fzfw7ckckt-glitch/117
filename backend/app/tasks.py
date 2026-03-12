from celery import Celery
from app.config import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "osint",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="test_task")
def test_task(query: str):
    logger.info(f"Processing test task with query: {query}")
    return {"result": f"Processed: {query}"}

@celery_app.task(name="run_maigret")
def run_maigret(username: str):
    logger.info(f"Running Maigret for username: {username}")
    # In production, call actual Maigret API
    return {"tool": "maigret", "username": username, "status": "completed"}

@celery_app.task(name="run_shodan")
def run_shodan(query: str):
    logger.info(f"Running Shodan query: {query}")
    # In production, call Shodan API
    return {"tool": "shodan", "query": query, "status": "completed"}
