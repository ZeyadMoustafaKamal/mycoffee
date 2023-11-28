from django.contrib import admin

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = 'pdf_file', 'stage'


admin.site.register(Report, ReportAdmin)
