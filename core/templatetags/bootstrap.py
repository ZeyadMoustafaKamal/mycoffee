from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='as_bootstrap')
def as_bootstrap(field):
    html = render_to_string('bootstrap/bootstrap_field.html', {'field': field})
    return mark_safe(html)
