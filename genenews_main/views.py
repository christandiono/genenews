# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.encoding import smart_str
from genenews_main.models import Article, Gene, Sequence, Vote
from genenews_main.forms import SubmissionForm

def index(request):
    articles = Article.objects.all().order_by('-pk')[:25]
    entries = add_votes(request, articles)
    return render_to_response('index.html',{'entries': entries}, context_instance=RequestContext(request))

@login_required
def submit(request):
    genes = []
    if request.method=="POST":
        form = SubmissionForm(request.POST)
        try:
            genes = [Gene.objects.get(pk=long(gene_id)) for gene_id in request.POST.getlist('gene')]
        except Gene.DoesNotExist:
            return HttpResponseForbidden()
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            map(lambda g: article.genes.add(g), genes)
            article.save()
            return HttpResponseRedirect(reverse('article', args=[article.id]))
    else:
        form = SubmissionForm()
    return render_to_response('submit.html', {'form': form, 'genes': genes}, context_instance=RequestContext(request))

@login_required
def gene_autocomplete(request):
    if request.method == "GET":
        if not request.GET.has_key('q') or not request.GET.has_key('limit'):
            return HttpResponseForbidden()
        try:
            int(request.GET.get('limit'))
        except ValueError:
            return HttpResponseForbidden()
        qtemp = Q(name__icontains=request.GET.get('q'))
        genes = Gene.objects.filter(qtemp)[:request.GET.get('limit', 10)]
        tempstr = '['
        for index, m in enumerate(genes):
            temp = {}
            temp['id'] = smart_str(m.id)
            temp['name'] = smart_str(m.medname())
            if index > 0:
                tempstr += ','
            tempstr += str(temp)
        tempstr += ']'
        return HttpResponse(tempstr, mimetype="application/json")
    resp = HttpResponse()
    resp.status_code = 405
    return resp

def gene_page(request, gene_name):
    gene = get_object_or_404(Gene, name=gene_name)
    articles = gene.article_set.all()
    entries = add_votes(request, articles)
    seq = gene.sequence
    return render_to_response('gene_page.html', {'gene': gene, 'entries': entries, 'seq':seq}, context_instance=RequestContext(request))

def add_votes(request, articles):
    if request.user.is_anonymous():
        return [(article, None, 0) for article in articles]

    else:
        out = []
        for article in articles:
            if article.vote_set.filter(user=request.user):
                out.append((article, article.vote_set.get(user=request.user), reduce(lambda x, y: x.vote+y.vote, article.vote_set.all(), Vote(vote=0))))
            else:
                out.append((article, None, 0))

        return out
