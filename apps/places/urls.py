from django.conf.urls.defaults import patterns, include, url

from api import PlaceResource
place_resource = PlaceResource()

from views import *

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    #url(r'^pt/(?P<id>\d+)/$', 'ajax_post_point', name="ajax_post_point"),
    #url(r'^post_test/$', index, name="index"),
    url(r'^post_test/$', post_handler, name="post_handler"),


    url(r'^admin/backup/?(?P<territoryno>[0-9\-]+)*/$', admin_backup, name="places_admin_backup"),
    url(r'^admin/restore/?(?P<territoryno>[0-9\-]+)*/$', admin_restore, name="places_admin_restore"),
    (r'^api/', include(place_resource.urls)),
)