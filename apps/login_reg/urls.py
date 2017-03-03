from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^process/login/(?P<id>\d+)$', views.success, name='success'),
	url(r'^process$', views.process, name='process'),
	url(r'^logout$', views.main, name='logout'),
    url(r'^$', views.main, name='main'),
]
