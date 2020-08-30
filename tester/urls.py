from django.urls import path

from . import views, examples

app_name='tester'

urlpatterns = [
    path('', views.submission_form, name='solve-default'),
    path('<str:assignment>/solve', views.submission_form, name='solve'),
    path('<str:assignment>/result', views.run_tests, name='runtests'),
    path('fibonacci-example', examples.nth_fibo, name='solution-example'),
]
