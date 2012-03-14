# -*- coding: utf-8 -*-
# boundaries/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

from tastypie.resources import ModelResource
from models import Boundary

#import wingdbstub

# curl http://localhost/api/v1/boundary/660/?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295;format=json
# curl http://localhost/api/v1/boundary/660/?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295;format=json
class ApiKeyPlusWebAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
	if request.user.is_authenticated():
	    return True
    
	return super(ApiKeyPlusWebAuthentication, self).is_authenticated(request, **kwargs)
    
    def get_identifier(self, request):
	if request.user.is_authenticated():
	    return request.user.username
	else:
	    return super(ApiKeyPlusWebAuthentication, self).get_identifier(request)

class BoundaryResource(ModelResource):
    class Meta:
        #queryset = Boundary.objects.all()
        queryset = Boundary.objects.filter(boundary_type = 5) # territories
        resource_name = 'boundary'        
        allowed_methods = ["get", "post", "put", "delete"]
        #excludes = ['isgeocoded', 'geo_name_id']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DjangoAuthorization()
    	# filtering = {
     #            'territoryno': ['exact'],
     #            #'user': ALL_WITH_RELATIONS,
     #            #'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
     #        }
	