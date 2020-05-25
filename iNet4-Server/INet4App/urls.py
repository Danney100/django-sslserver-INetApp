"""INetApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', view=views.Login, name='Login'),
    url(r'^HomePage/$', view=views.HomePage, name='HomePage'),
    url(r'^ListjobAjax/$', view=views.ListjobAjax, name='ListjobAjax'),
    url(r'^CompleteJob/$', view=views.CompleteJob, name='CompleteJob'),
    url(r'^ReturnJob/$', view=views.ReturnJob, name='ReturnJob'),
    url(r'^SignJobout/$', view=views.SignJobout, name='SignJobout'),
    url(r'^SavingJob/$', view=views.SavingJob, name='SavingJob'),
]
