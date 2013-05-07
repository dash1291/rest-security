from django.conf.urls import patterns, include, url

from .views import *

urlpatterns += patterns('',
	url('session_token/', generate_session_token),
)