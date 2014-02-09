from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from topics import views

urlpatterns = patterns('',
    url(r'^$', views.all_topics, name='all_topics'),
    url(r'^/(?P<slug>[-\w]+)', views.view_topic, name='view_topic'),
)