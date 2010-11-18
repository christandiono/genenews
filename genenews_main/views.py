# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from genenews_main.models import Article

def index(request):
    articles = Article.objects.all()[:10]
    return render_to_response('index.html',{'articles': articles}, context_instance=RequestContext(request))
