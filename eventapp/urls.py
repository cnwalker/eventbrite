from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import eventfinder.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eventapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', eventfinder.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/', eventfinder.views.events, name='events'),
)
