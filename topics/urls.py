from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from topics import views

urlpatterns = patterns('',
    url(r'^$', views.all_topics, name='all_topics'),
    url(r'^(?P<slug>[-\w]+)', views.view_topic, name='view_topic'),
    url(r'^create_topic/', views.create_topic, name='create_topic'),
    url(r'^add_vocab/(?P<topic_slug>[-\w]+)', views.add_vocab, name='add_vocab'),
    url(r'^add_link/(?P<topic_slug>[-\w]+)', views.add_link, name='add_link'),
    url(r'^add_information/(?P<topic_slug>[-\w]+)', views.add_information, name='add_information'),
    url(r'^add_problem/(?P<topic_slug>[-\w]+)', views.add_problem, name='add_problem'),
)