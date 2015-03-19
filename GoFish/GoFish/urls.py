from django.conf.urls import patterns, include, url
from django.contrib import admin
from game import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', include('game.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^lobby$', views.lobby, name='lobby'),
    url(r'^lobby/(?P<game_id>[0-9]+)/$', views.lobby, name='lobby'),
)
