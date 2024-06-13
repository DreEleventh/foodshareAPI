# app.py
from celery import Celery

celery_app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

# tasks.py
# from app import celery_app


@celery_app.task
def send_notification(recipient_id, message):
    # Logic to send the notification (e.g., email, push notification, etc.)
    pass
