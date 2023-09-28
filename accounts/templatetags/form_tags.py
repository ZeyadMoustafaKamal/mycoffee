from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from functools import lru_cache

register = template.Library()

@lru_cache() # cache it
@register.filter(name='as_bootstrap')
def as_bootstrap(form):
    html = """  """
    field_keys = list(form.fields.keys())
    for index, field in enumerate(form):
        field_obj = field.field
        if index == 0:
            if hasattr(field_obj, 'col_value'):
                html += '<div class="form-row">'
        else:
            if hasattr(field_obj, 'col_value'):
                prev_field = form[field_keys[index-1]].field
                if not hasattr(prev_field, 'col_value'):
                    html += '<div class="form-row">'
        html += render_field(field)
        if not index == len(form.fields.items()) - 1:
            next_field = form[field_keys[index+1]].field
            if hasattr(field_obj, 'col_value') and not hasattr(next_field, 'col_value'):
                html += '</div>\n'
    return mark_safe(html)

def render_field(field):
    col_value = getattr(field.field, 'col_value', None)
    context = {
        'col_value':col_value,
        'field':field
    }
    html = render_to_string('bootstrap/field.html', context)
    return html