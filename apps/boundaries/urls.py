from django.conf.urls.defaults import patterns, include, url

from api import BoundaryResource
boundary_resource = BoundaryResource()

from views import *

urlpatterns = patterns('',
    (r'^api/', include(boundary_resource.urls)),
)