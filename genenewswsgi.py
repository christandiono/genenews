import sys

sys.path.append('/usr/local/var/genenews')
sys.path.append('/usr/local/var')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'genenews.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
