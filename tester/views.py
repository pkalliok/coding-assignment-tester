from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

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

def save_test_results(assignment, endpoint, results):
    sub = Submission(submission_endpoint_address=endpoint,
            assignment_name=assignment, submission_time=timezone.now())
    sub.save()
    for inp, result in results:
        sub.passedtest_set.create(test_input=inp, test_output=result)
    return sub

def run_tests(request, **kw):
    assignment=kw['assignment']
    try: endpoint = request.POST['endpoint_url']
    except KeyError:
        return HttpResponseBadRequest('Missing parameter: endpoint_url')
    try: results = run_tests_against(assignment, endpoint)
    except FailedTest as e:
        return render(request, 'tester/failed_test.jinja',
                {**jinja_context, **e.content})
    submission = save_test_results(assignment, endpoint, results)
    return HttpResponseRedirect(reverse('tester:results',
                        args=(assignment, submission.id,)))

def show_results(request, **kw):
    submission = get_object_or_404(Submission, id=kw['submission'],
            applicant_address='', submission_code_address='')
    return render(request, 'tester/result_report.jinja',
            {**jinja_context, **kw, 'results': submission})

def save_submission(request, **kw):
    submission = get_object_or_404(Submission, id=kw['submission'],
            assignment_name=kw['assignment'],
            submission_endpoint_address=request.POST['endpoint_url'])
    submission.applicant_address = request.POST['applicant_address']
    submission.submission_code_address = request.POST['source_code_url']
    submission.save()
    return render(request, 'tester/submission_accepted.jinja',
            {**jinja_context, **kw, 'results': submission})

