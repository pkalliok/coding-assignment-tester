from django.urls import path

from . import views, examples

app_name='tester'

urlpatterns = [
    path('', views.submission_form, name='solve-default'),
    path('<str:assignment>/solve', views.submission_form, name='solve'),
    path('<str:assignment>/check', views.run_tests, name='runtests'),
    path('<str:assignment>/result/<int:submission>', views.show_results,
        name='results'),
    path('<str:assignment>/submit/<int:submission>', views.save_submission,
        name='savesubmission'),
    path('fibonacci-example', examples.nth_fibo, name='solution-example'),
]
