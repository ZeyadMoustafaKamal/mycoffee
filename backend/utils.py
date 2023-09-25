from django.shortcuts import render


def render_htmx(request, normal_template, partial_template, context=None):
    if request.htmx:
        return render(request, partial_template, context)
    return render(request, normal_template, context)
