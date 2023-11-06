from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured


class SuccessMessageMixin:
    success_message = None

    def form_valid(self, *args, **kwargs):
        messages.success(self.request, self.get_success_message())
        return super().form_valid(*args, **kwargs)

    def get_success_message(self):
        if self.success_message is not None:
            return self.success_message
        raise ImproperlyConfigured(
            'There is no success_message in %s please set one or override get_success_message'
            % self.__class__.__name__
        )
