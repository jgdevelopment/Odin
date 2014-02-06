from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create_account/', views.create_account, name='create_account')
)