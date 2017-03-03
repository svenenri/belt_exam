from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
	url(r'^add/process/join/(?P<id>\d+)$', views.join, name='join'),
	url(r'^add/process$', views.process, name='process'),
	url(r'^add$', views.add, name='add'),
    url(r'^$', views.travel, name='travel'),
]
