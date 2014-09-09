from django.conf.urls import patterns, url
from firewall import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^fault$', views.Fault.as_view(), name='fault'),
    url(r'^welcome$', login_required(views.Welcome.as_view(), login_url = '/'), name='welcome'),
)
