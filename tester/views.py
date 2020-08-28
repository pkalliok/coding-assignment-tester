from django.shortcuts import render
from django.http import HttpResponse

def submission_form(request, assignment='fibonacci'):
    return render(request, 'tester/submission_form.jinja',
            {'assignment': assignment})

