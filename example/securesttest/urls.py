from django.conf.urls import patterns, include, url

from views import *
from securest.modules.djangosecurest.views import generate_session_token

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url('^test/$', test),
	url('^create_cert/$', app_signup),
	url('^register/$', register_user),
	url('^session_token/$', generate_session_token),
    # Examples:
    # url(r'^$', 'securesttest.views.home', name='home'),
    # url(r'^securesttest/', include('securesttest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
