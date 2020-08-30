from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse

from .models import Submission, PassedTest
from .testing import run_tests_against, FailedTest

jinja_context = dict(
        assignment='fibonacci',
        url=reverse,
        static=static,
)

def submission_form(request, **kw):
    return render(request, 'tester/submission_form.jinja',
            {**jinja_context, **kw})

def run_tests(request, **kw):
    try: endpoint = request.POST['endpoint_url']
    except KeyError:
        return HttpResponseBadRequest('Missing parameter: endpoint_url')
    try: results = run_tests_against(kw['assignment'], endpoint)
    except FailedTest as e:
        return render(request, 'tester/failed_test.jinja',
                {**jinja_context, **e.content})
    return render(request, 'tester/result_report.jinja',
            {**jinja_context, **kw})

