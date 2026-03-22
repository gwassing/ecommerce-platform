from django.core.mail import send_mail
from django_tasks import task


@task
def send_order_confirmation(message, recipient):
    return send_mail(
        "Thank you for your order!",
        message,
        "info@gabylando.com",
        [recipient],
    )
