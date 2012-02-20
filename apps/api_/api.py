# -*- coding: utf-8 -*-
# tweets/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from .models import Tweet

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

class TweetResource(ModelResource):
    class Meta:
        queryset = Tweet.objects.all()
        #resource_name = 'tweet'        
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DjangoAuthorization()