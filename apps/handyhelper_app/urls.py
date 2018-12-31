from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard), 
    url(r'^logout$', views.logout),
    url(r'^addjob$', views.add),
    url(r'^jobs/create', views.create),
    url(r'^view/(?P<job_id>\d+)$', views.show),
    url(r'^edit/(?P<job_id>\d+)$', views.edit),
    url(r'^editjob/(?P<job_id>\d+)$', views.editjob),
    url(r'^delete/(?P<job_id>\d+)$', views.delete),
    url(r'^addtomyjobs/(?P<job_id>\d+)$', views.addtomyjobs),
]