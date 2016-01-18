from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import eventfinder.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eventapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', eventfinder.views.index, name='index'),
    url(r'^db', eventfinder.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

)
