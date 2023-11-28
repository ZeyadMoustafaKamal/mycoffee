from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML

from orders.models import Order

from .models import Report

User = get_user_model()


@shared_task()
def generate_report(report_id):
    """ Generate a PDF file for the given report instance. """
    first_day = timezone.now().replace(day=1)  # first day of the current month

    users_this_month = User.objects.filter(date_joined__gte=first_day)
    users_last_28_days = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=28))

    orders_done_this_month = Order.objects.filter(status='Done', created_at__gte=first_day)

    profit_this_month = sum([order.get_total for order in orders_done_this_month])

    context = {
        'users_last_month': users_this_month.count(),
        'users_last_28_days': users_last_28_days.count(),
        'orders_done_this_month': orders_done_this_month.count(),
        'profile_this_month': profit_this_month
    }
    report_string = render_to_string('reports/report_template.html', context=context)
    pdf_file = HTML(string=report_string).write_pdf()

    report = Report.objects.get(id=report_id)
    report.pdf_file.save('report.pdf', ContentFile(pdf_file), False)
    report.stage = report.StageChoices.done
    report.save()
