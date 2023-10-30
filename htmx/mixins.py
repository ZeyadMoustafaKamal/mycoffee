from .base import HTMXRedirect


class HTMXTemplateMixin:
    htmx_template = None

    def get_template_names(self):
        if self.request.htmx and self.htmx_template:
            return [self.htmx_template]
        return super().get_template_names()


class HTMXRedirectMixin:
    def form_valid(self, form):
        super().form_valid(form)
        return HTMXRedirect(self.get_success_url())
