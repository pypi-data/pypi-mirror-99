from django.conf import settings
from django.utils.translation import ugettext as _
import os


DEBUG = getattr(settings, 'DEBUG')
BASE_DIR = getattr(settings, 'BASE_DIR')
STRING_SINGLE = getattr(settings, 'STRING_SINGLE')
STRING_SHORT = getattr(settings, 'STRING_SHORT')
STRING_MEDIUM = getattr(settings, 'STRING_MEDIUM')
STRING_NORMAL = getattr(settings, 'STRING_NORMAL')
STRING_LONG = getattr(settings, 'STRING_LONG')
STRING_DOUBLE = getattr(settings, 'STRING_DOUBLE')
HOST = getattr(settings, 'HOST')
SUBDOMAINS = getattr(settings, 'SUBDOMAINS')
PROTOCOL = getattr(settings, 'PROTOCOL')
HOSTNAME = getattr(settings, 'HOSTNAME')
WEBSITE_URL = getattr(settings, 'WEBSITE_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
ADMINS = getattr(settings, 'ADMINS', [])

APP = 'MATIALVAREZS_HANDLERS_EASY_'

VARIABLE = getattr(settings, APP + 'VARIABLE', None)

SCRIPTS_PATH = getattr(settings, 'SCRIPTS_PATH')
CRON_JOB_LOGS_PATH = getattr(settings, 'CRON_JOB_LOGS_PATH')
CRONTAB_USER = getattr(settings,'CRONTAB_USER')