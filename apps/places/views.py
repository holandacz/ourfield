#import wingdbstub
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Place


def home(request):
    """ Homepage """
    return render_to_response("home/base.html", locals(), context_instance=RequestContext(request))
