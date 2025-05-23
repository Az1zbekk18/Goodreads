from django.core.mail import send_mail
from goodreads.celery import app
from django.conf import settings

@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
