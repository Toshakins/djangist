from django.conf.urls import patterns, url
from firewall import views

urlpatterns = patterns('',
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^fault$', views.fault, name='fault'),
    url(r'^$', views.index, name='index'),
)
