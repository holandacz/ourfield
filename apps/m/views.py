from django.template import RequestContext
from django.shortcuts import render_to_response

from tastypie.models import ApiKey 
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
    
    # grab tastypie api_key for current user
    # QUESTION: way to send json blog of current user to js app?
    api_key = usergroups = ''
    userisstaff = userissuperuser = 0
    if request.user.is_authenticated():
        api_key = ApiKey.objects.get(id=request.user.id)
        usergroups = ','.join([group.name for group in usergroups])
        userisstaff = 1 if request.user.is_staff else 0
        userissuperuser = 1 if request.user.is_superuser else 0
        
    territoryno = request.GET.get('territoryno', '')
    print territoryno
    request.session['territoryno'] = territoryno
    context = {
        'user' : request.user,
        'usergroups' : usergroups,
        'userisstaff' : userisstaff,
        'userissuperuser' : userissuperuser,
        'api_key' : api_key,
        'center' : request.GET.get('ll', ""),
        'zoom' : request.GET.get('z', 0),
        'territoryno' : territoryno,
        'polys' : polys,
        'enpts' : enpts,
        'placepts' : placepts,
    }
    return render_to_response("m/base.html", locals(), context_instance=RequestContext(request, context))
