#urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^tweeting/$', views.tweeting, name='tweeting'),
	url(r'^classify/$', views.classify, name='classify'),
	url(r'^about/$', view.about, name='about'),
]