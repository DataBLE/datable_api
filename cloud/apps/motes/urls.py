from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
        url('^confirm$', views.mote_confirm, name='mote-confirm'),
        url('^discover$', views.mote_discovered, name='mote-discovered'),
        url('^sighting$', views.mote_sighting, name='mote-sighting'),
        url('^app$', views.mote_app, name='mote-app'),
        )
