from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Report(models.Model):
    class StageChoices(models.Choices):
        preparing = 'Preparing'
        done = 'Done'

    pdf_file = models.FileField(max_length=200, null=True, blank=True)
    stage = models.CharField(max_length=100, choices=StageChoices.choices, default=StageChoices.preparing)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_reports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stage}, {self.created_at}'
