from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from genenews.genenews_main.models import Article

def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render_to_response('articles/index.html', {'article': article}, context_instance=RequestContext(request))

