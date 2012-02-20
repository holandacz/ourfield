from django.views.decorators.csrf import csrf_exempt 
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Place
from django.utils import simplejson as json

#import wingdbstub

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

