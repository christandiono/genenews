from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^login/$', 'user_auth.views.login', name='auth_login'),
    url(r'^logout/$',
        'user_auth.views.logout',
        name='auth_logout'),
    url(r'^password/change/$',
        'user_auth.views.password_change',
        name='auth_password_change'),
    url(r'^password/change/done/$',
        'user_auth.views.password_change_done',
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        'user_auth.views.password_reset',
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'user_auth.views.password_reset_confirm',
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        'user_auth.views.password_reset_complete',
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        'user_auth.views.password_reset_done',
        name='auth_password_reset_done'),
    url(r'^forwardemail/$',
        'user_auth.views.set_forward_email',
        name='set_forward_email'),
    url(r'^test/login/$',
        'user_auth.views.login_test',
        name='login_test'),
    url(r'^create/$',
        'user_auth.views.register',
        name='register'),
) 
