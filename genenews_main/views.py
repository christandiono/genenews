# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import smart_str
from genenews_main.models import Article, Gene
from genenews_main.forms import SubmissionForm

def index(request):
    articles = Article.objects.all()[:25]
    return render_to_response('index.html',{'articles': articles}, context_instance=RequestContext(request))

@login_required
def submit(request):
    if request.method=="POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            try:
                genes = [Gene.objects.get(pk=long(attendee_id)) for attendee_id in request.POST.getlist('gene')]
            except Gene.DoesNotExist:
                return HttpResponseForbidden()
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            map(lambda g: article.genes.add(g), genes)
            article.save()
            return HttpResponseRedirect(reverse('article', args=[article.id]))
    else:
        form = SubmissionForm()
    return render_to_response('submit.html', {'form': form}, context_instance=RequestContext(request))


def gene_autocomplete(request):
    if request.method == "GET":
        if not request.GET.has_key('q') or not request.GET.has_key('limit'):
            return HttpResponseForbidden()
        try:
            int(request.GET.get('limit'))
        except ValueError:
            return HttpResponseForbidden()
        genes = Gene.objects.filter(name__icontains=request.GET.get('q'))[:request.GET.get('limit', 10)]
        tempstr = '['
        for index, m in enumerate(genes):
            print index
            temp = {}
            temp['id'] = smart_str(m.id)
            temp['name'] = smart_str(m.name)
            if index > 0:
                tempstr += ','
            tempstr += str(temp)
        tempstr += ']'
        return HttpResponse(tempstr, mimetype="application/json")
    resp = HttpResponse()
    resp.status_code = 405
    return resp
