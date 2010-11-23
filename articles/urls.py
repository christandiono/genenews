from django.conf.urls.defaults import *    

urlpatterns = patterns('articles.views',
    url(r'(?P<article_id>\d+)/$', 'show_article', name='article'),
) 
