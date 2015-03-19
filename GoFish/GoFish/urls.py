from django.conf.urls import patterns, include, url
from django.contrib import admin
from game import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', include('game.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^lobby$', views.lobby, name='lobby'),
)
