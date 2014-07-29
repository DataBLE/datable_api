"""Settings for Development Server"""
from cloud.settings.base import *   # pylint: disable=W0614,W0401

import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#VAR_ROOT = '/var/www/cloud'
#MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
#STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'cloud',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpassword',
#    }
#}


# TODO: This is needed because the heroku buildpack is currently messed up
# http://stackoverflow.com/questions/22361094/heroku-django-could-not-import-user-defined-geometry-backend-geos
import os
GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(os.environ.get('GEOS_LIBRARY_PATH'))
GDAL_LIBRARY_PATH = "{}/libgdal.so".format(os.environ.get('GDAL_LIBRARY_PATH'))


DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
SOCKET_HOST='174.129.231.63'
SOCKET_PORT=9091

#WSGI_APPLICATION = 'cloud.wsgi.application'
