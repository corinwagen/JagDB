from django.http import HttpResponse
from django.shortcuts import render
import datetime

def home(request):
    context = {}
#    if request.session['user']:
#        context.user = request.session['user']
#    else:
    user = {'name': 'ari'}
    context['user'] = user
    return render(request, 'home.html', context)

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)    

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
