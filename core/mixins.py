
class HTMXTemplateMixin:
    htmx_template = None
    def get_template_names(self):
        if self.request.htmx and self.htmx_template:
            return [self.htmx_template]
        return super().get_template_names()
