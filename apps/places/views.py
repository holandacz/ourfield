from django.views.decorators.csrf import csrf_exempt 
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Place
from django.utils import simplejson as json

#import wingdbstub
    
def admin_updatemarkernos(request):
    from markernos import PlaceMarkernos
    from django.http import HttpResponseRedirect
    
    territoryno = request.session.get('territoryno')

    if not territoryno:
        raise ValueError("No territoryno!")
    
    # get places that need to be assigned numbers based on routemarkernoafter in descending order
    for place in Place.objects.filter(territoryno=territoryno).filter(routemarkernoafter__gt=0).order_by("-routemarkernoafter"):
        print place.routemarkernoafter
        
        placeMarkernos = PlaceMarkernos(place)        
        placeMarkernos.updateMarkernos()
        
    return HttpResponseRedirect("/map/?territoryno=%s" % territoryno)    
    
def admin_automarkerno(request, id = None):
    from django.http import HttpResponseRedirect
    from markernos import PlaceMarkernos
    
    territoryno = request.session.get('territoryno')

    if not territoryno:
        error = "No territoryno!"
        return HttpResponse('ERROR: %s' % error)
    
    start_id = request.session.get('id', id) 
    
    placeMarkernos = PlaceMarkernos() 
    retval = placeMarkernos.automarkerno(start_id=id, territoryno=territoryno)    
    
    if not retval == True:
        raise ValueError(retval)
    
    return HttpResponseRedirect("/map/?territoryno=%s" % territoryno)


def ajax_route(request, id):
    from markernos import PlaceMarkernos
    
    placeMarkernos = PlaceMarkernos() 
    retval = placeMarkernos.automarkerno(start_id=id)     

    if not retval == True:
        return HttpResponse(retval)
    else:
        return HttpResponse('')
    

def admin_restore(request, territoryno = None):
    from django.db import connection
    from django.http import HttpResponseRedirect

    #return HttpResponse('')

    territoryno = request.session.get('territoryno', territoryno)
    # SQL DELETE
    if not territoryno:
        raise ValueError("No territoryno!")

    cursor = connection.cursor()
    sql = 'DELETE FROM %s WHERE territoryno = "%s"' % (Place._meta.db_table, territoryno)
    cursor.execute(sql)

    # clone Places 
    places = Place.objects.filter(territoryno = '_' + territoryno)
    for place in places:
        place.id = None
        place.territoryno = territoryno
        place.save(handleMarkernos = False)

    return HttpResponseRedirect("/map/?territoryno=%s" % territoryno)

def admin_backup(request, territoryno = None):
    from django.db import connections, connection, transaction
    #return HttpResponse('')

    territoryno = request.session.get('territoryno', territoryno)
    # SQL DELETE
    if not territoryno:
        raise ValueError("No territoryno!")

    #cursor_live = connections['live'].cursor()
    #print cursor_live
    #exit()

    cursor = connection.cursor()
    sql = 'DELETE FROM %s WHERE territoryno = "_%s"' % (Place._meta.db_table, territoryno)
    cursor.execute(sql)

    # clone Places 
    places = Place.objects.filter(territoryno=territoryno)
    for place in places:
        place.id = None
        place.territoryno = '_' + territoryno
        place.save(handleMarkernos = False)



    return render_to_response("places/base.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def post_handler(request, *args, **kwargs):
    #if request.is_ajax() and request.method == 'POST':
    if request.method == 'POST':
        post = request.POST
        id = int(post['id'])
        place = Place.objects.get(id=id)
        point = 'POINT(%s %s)' % (post['lat'], post['lng'])
        place.point = point
        place.save()
        
    return HttpResponse("")


def get_point(request, id):
    try:
        place = Place.objects.get(id=id)
        response_data = {'lat': place.point.x, 'lng':place.point.y}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    except:
        return HttpResponse("")


#def ajax_post_point(request):
    #post_text = request.POST['post_data']
    #return HttpResponse("{'response_text': '"+post_text+" recieved.'}",
                                   #mimetype="application/json")
                                
def index(request):
    #return HttpResponse('')
    return render_to_response("places/base.html", locals(), context_instance=RequestContext(request))

def get_pts():
    pts = Place.objects.filter(isgeocoded = True)
    return pts

