"""CodeforcesCrawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from cfhandler import views as cfviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home, name='home'),
    path('timetable', views.timetable, name='timetable'),
    path('iitg', views.iitg, name='iitg'),
    path('cfhandler/cfsearch/<str:handle>', cfviews.userprofile, name='userprofile'),
    path('cfhandler/contest/<str:handle>', cfviews.contest, name='contest-statistics'),
    path('search', views.search, name='search'),
    path('accounts/', include('accounts.urls')),
    path('cfhandler/', include('cfhandler.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
