from django.shortcuts import render
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse

jinja_context = dict(
        assignment='fibonacci',
        url=reverse,
        static=static,
)

def submission_form(request, **kw):
    return render(request, 'tester/submission_form.jinja',
            {**jinja_context, **kw})

def run_tests(request, **kw):
    return render(request, 'tester/result_report.jinja',
            {**jinja_context, **kw})

