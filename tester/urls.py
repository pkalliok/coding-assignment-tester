from django.urls import path

from . import views

urlpatterns = [
    path('', views.submission_form, name='solve-default'),
    path('<str:assignment>/solve', views.submission_form, name='solve'),
]
