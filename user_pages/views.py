from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from genenews.genenews_main.models import Article, LeaderboardCache, get_user_score
from genenews.genenews_main.views import add_votes

def index(request, user_name):
    user = get_object_or_404(User, username=user_name)
    entries = add_votes(request, user.article_set.all())
    user_points = 0
    for entry in entries:
        article = entry[0]
    user_points = get_user_score(user)
    try:
        user_rank = LeaderboardCache.objects.get(user=user, type='all').rank
    except LeaderboardCache.DoesNotExist:
        user_rank = None # do nothing; won't show up in template anyway
    return render_to_response('user_pages/index.html', {'user': user, 'entries': entries, 'user_points': user_points, 'user_rank': user_rank}, context_instance=RequestContext(request))

