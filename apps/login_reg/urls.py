from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^process$', views.process, name='process'),
	url(r'^logout$', views.logout, name='logout'),
    url(r'^$', views.main, name='main'),
]
