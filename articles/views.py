from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from genenews.genenews_main.models import Article, Vote
from genenews.genenews_main.views import add_votes

import simplejson as json

def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    [(article, vote, points)] = add_votes(request, [article])
    related = []
    for gene in article.genes.all():
        for a in gene.article_set.all():
            if a.id != article.id:
                related.append(a)
    likes = 0
    dislikes = 0
    for v in article.vote_set.all():
        if v.vote == 1:
            likes += 1
        elif v.vote == -1:
            dislikes +=1
    entries = add_votes(request, related)
    return render_to_response('articles/index.html', {'article': article, 'vote': vote, 'points': points, 'entries': entries, 'likes': likes, 'dislikes': dislikes}, context_instance=RequestContext(request))

@login_required
def vote(request):
    if request.method == "POST":
        direction_dict = {'up': 1, 'down': -1}
        direction = request.POST.get('direction')
        article_id = request.POST.get('article_id')
        vote = direction_dict[direction]
        article = get_object_or_404(Article, id=article_id)
        try:
            vote_object = Vote.objects.get(article=article, user=request.user)
            if vote_object.vote != vote:
                vote_object.vote = vote
                vote_object.save()
                color_this = True
                changed_other = True
            else:
                vote_object.delete()
                color_this = False
                changed_other = False
        except Vote.DoesNotExist:
            vote_object = Vote(vote=vote, article=article, user=request.user)
            vote_object.save()
            color_this = True
            changed_other = False

        return HttpResponse(json.dumps({'direction': direction, 
            'changed_other': changed_other, 
            'id': article_id, 
            'color_this': 'mod' if color_this else 'gray'}), mimetype="application/json")
    else:
        HttpRepsonse('', mimetype="text/plain")


