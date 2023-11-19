from celery import shared_task

from .models import Report


@shared_task()
def generate_report(user=None):
    """ Generate a report instance in the background
    if user passed put it in the requested_by of the report instance
    """
    report = Report.objects.create(requested_by=user)  # noqa: F841
