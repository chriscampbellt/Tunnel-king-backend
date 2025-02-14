from celery import shared_task
from django.core.mail import send_mail

from apps.organization.models import Organization


@shared_task
def send_reset_email_task(organization_id, organization_name, email, reset_link):
    """
    Celery task to send the password reset email.
    """

    try:
        send_mail(
            subject="Set Your Admin Password",
            message=f"Welcome to {organization_name}!\n\nPlease set your "
            f"password using the link below:\n\n{reset_link}\n\n"
            f"If you did not request this, please ignore this email.",
            from_email="no-reply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        # Update the organization's email_sent flag on success
        Organization.objects.filter(id=organization_id).update(email_sent=True)
    except Exception as e:
        # Log or handle the exception as needed
        Organization.objects.filter(id=organization_id).update(email_sent=False)
        raise e
