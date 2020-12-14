from django.urls import path

from . import views


urlpatterns = [
    path("timetable", views.timetable, name="timetable"),
    path("iitg", views.iitg, name="iitg"),
    path("searchhandle", views.cfsearch, name="searchhandle"),
]