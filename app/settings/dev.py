'''
    Local Development settings override

'''

from .base import *

DEBUG = True

INSTALLED_APPS += [
    'django_extensions',
]
EMAIL_HOST_USER = get_key('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_key('EMAIL_HOST_PASSWORD')


