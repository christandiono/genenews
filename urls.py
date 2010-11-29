from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^genenews/', include('genenews.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('user_auth.urls')),
    url(r'^article/', include('articles.urls')),
    (r'^user/', include('genenews.user_pages.urls')),
    url(r'^submit/$', 'genenews_main.views.submit', name='submit'),
    url(r'^submit/autocomplete/$', 'genenews_main.views.gene_autocomplete', name='gene_autocomplete'),
    url(r'^$', 'genenews_main.views.index', name="index"),
    url(r'^gene/(?P<gene_name>.*)/$', 'genenews_main.views.gene_page', name='gene_page'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/chris/genenews/media'}),
        (r'^jbrowse/$', 'django.views.static.serve', {'document_root': '/home/chris/jbrowse_temp/jbrowse/'}),
        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/chris/genenews/static'}),
    )
else:
    urlpatterns += patterns('',
        url(r'^uwsgi_admin/', include('uwsgi_admin.urls')),
        )
