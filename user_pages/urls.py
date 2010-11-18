from django.conf.urls.defaults import *    

urlpatterns = patterns('user_pages.views',
    url(r'(?P<user_name>.+)/$', 'index', name='user-index'),
) 
