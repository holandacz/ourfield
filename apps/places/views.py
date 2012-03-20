from django.views.decorators.csrf import csrf_exempt 
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Place
from django.utils import simplejson as json

#import wingdbstub


def admin_automarkerno(request, id = None):
    from django.db import connection
    from django.http import HttpResponseRedirect
    
    territoryno = request.session.get('territoryno')

    if not territoryno:
        raise ValueError("No territoryno!")

    start_id = request.session.get('id', id)

    # try with 3
    # start_id = 2846

    # if a start_id given, get marker number for that id
    if start_id:
        try:
            startPlace = Place.objects.get(id=start_id)
        except:
            raise ValueError('Invalid ID: %d' % start_id)

        start_markerno = startPlace.markerno
        
        # if are there Places that have markerno's before this markerno?
        for markerno in range(1, start_markerno):
            if not Place.objects.filter(territoryno=territoryno).filter(markerno=markerno).exists():
                raise ValueError('Expected a Place with markerno = : %d' % markerno)
        
        # if no more places to number
        if len(Place.objects.all()) == start_markerno:
            return
        
        place = startPlace
        markerno = start_markerno + 1 # we already have start_markerno set
        while True:
            
            # find closest Place with markerno greater than place.markerno
            place = place.findClosestPlace(place.markerno)
            if not place:
                break
            place.markerno = markerno
            place.save(handleMarkernos = False)
            markerno += 1
            
    else:
        # number all Places
        places = Place.objects.filter(territoryno = territoryno)
        if not places:
            return
        
        # Reset all markerno's
        Place.objects.filter(territoryno=territoryno).update(markerno=0)
        
        # find west / left most Place within territory        
        westPlaceLng = 999999
        startPlace = None
        for place in places:        
            if place.point[1] < westPlaceLng:
                westPlaceLng = place.point[1]
                startPlace = place
            
            
        start_markerno = 1    
        startPlace.markerno = start_markerno
        startPlace.save(handleMarkernos = False)
        place = startPlace
        markerno = start_markerno + 1 # we already have start_markerno set
        
        # loop through all places in territory
        while True:
            
            # find closest Place with markerno greater than place.markerno
            place = place.findClosestPlace(place.markerno)
            if not place:
                break
            place.markerno = markerno
            place.save(handleMarkernos = False)
            markerno += 1
        
        

    return HttpResponseRedirect("/map/?territoryno=%s" % territoryno)



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

