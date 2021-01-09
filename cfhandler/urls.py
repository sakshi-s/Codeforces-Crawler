from . import views
from django.urls import path


app_name = 'cfhandler'

urlpatterns = [
    path("timetable", views.timetable, name = "timetable"),
    path("iitg", views.iitg, name = "iitg"),
    path("cfsearch", views.cfsearch, name = "cfsearch")
]