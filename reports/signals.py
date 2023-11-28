from django.db.models.signals import post_save
from django.dispatch import receiver

from reports.tasks import generate_report

from .models import Report


@receiver(post_save, sender=Report)
def create_report_handler(instance, created, *args, **kwargs):
    if created:
        generate_report.delay(instance.pk)
