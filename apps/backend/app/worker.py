import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("egysaas", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def send_welcome_email(email: str):
    # Replace with real email integration
    print(f"[celery] Sending welcome email to {email}")
    return True
