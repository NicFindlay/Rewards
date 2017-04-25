from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .models import Profile

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send/', views.send, name='send'),
    url(r'^thanks/', views.thanks, name='thanks'),

    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),


]