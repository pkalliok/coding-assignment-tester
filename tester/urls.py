from django.urls import path

from . import views

app_name='tester'

urlpatterns = [
    path('', views.submission_form, name='solve-default'),
    path('<str:assignment>/solve', views.submission_form, name='solve'),
    path('<str:assignment>/result', views.run_tests, name='runtests'),
]
