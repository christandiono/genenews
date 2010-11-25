from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from genenews.genenews_main.models import Article
from genenews.genenews_main.views import add_votes

def index(request, user_name):
    user = get_object_or_404(User, username=user_name)
    articles = add_votes(request, Article.objects.filter(user=user))
    return render_to_response('user_pages/index.html', {'user': user, 'articles': articles}, context_instance=RequestContext(request))

