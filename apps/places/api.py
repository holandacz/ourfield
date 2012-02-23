# -*- coding: utf-8 -*-
# places/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

from tastypie.resources import ModelResource
from models import Place

# curl http://localhost/api/v1/place/660/?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295;format=json
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

class PlaceResource(ModelResource):
    class Meta:
        # queryset = Place.objects.all()
        queryset = Place.objects.filter(geocoded = True)
        resource_name = 'place'        
        allowed_methods = ["get", "post", "put", "delete"]
        excludes = ['isgeocoded', 'googlemapurl', 'geo_name_id']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DjangoAuthorization()