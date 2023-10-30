import json

from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render


class HTMXRedirect(HttpResponseRedirectBase):
    status_code = 200

    def __init__(self, redirect_to, full_page=True, *args, **kwargs):
        super().__init__(redirect_to, *args, **kwargs)
        self['HX-Location'] = self['Location']
        if full_page:
            headers = {
                'path': self['Location'],
                'headers': {
                    'HX-Fullpage': 'true'
                }
            }
            self['HX-Location'] = json.dumps(headers)
        del self['Location']


def render_htmx(request, normal_template, partial_template, context=None):
    if request.htmx:
        return render(request, partial_template, context)
    return render(request, normal_template, context)
