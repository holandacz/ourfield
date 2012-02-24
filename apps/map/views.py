from django.template import RequestContext
from django.shortcuts import render_to_response

from places.views import get_pts as get_placepts
from en.views import get_pts as get_enpts
#import wingdbstub

def index(request):
    """ Homepage """
    #if request.user.is_superuser:
        #polys = None
        #enpts = None
        #placepts = None
    #if request.user.is_staff:
        #polys = get_polys()
        #enpts = get_enpts()
        #placepts = get_placepts()
    #else:
        #enpts = None
        #enpts = None
        #placepts = None

    polys = None
    enpts = None
    placepts = None
    # placepts = get_placepts()
    context = {
        'user' : request.user,
        'center' : request.GET.get('ll', ""),
        'zoom' : request.GET.get('z', 0),
        'polys' : polys,
        'enpts' : enpts,
        'placepts' : placepts,
    }
    return render_to_response("map/base.html", locals(), context_instance=RequestContext(request, context))
