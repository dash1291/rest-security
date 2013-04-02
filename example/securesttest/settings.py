# Django settings for securesttest project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'securestdb.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j+)xve3tfyu-t!@d6&amp;k&amp;fbj!f5hq%k)!-a@7h182j1ecl**hym'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'securest.modules.djangosecurest.utils.Middleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'securesttest.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'securesttest.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'securest.modules.djangosecurest'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SECUREST_SERVER_CERTIFICATE_ID = 'cert123'
SECUREST_PRIVATE_KEY = '-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQCxKrTkA3UVbziDZwPlsQY5zJBE4riPZaakJZSwgAQ6bkKpvJuM\nlOIN0eRQ/eZMwMtOnVqWDWCiMujHiwyFxbFR12WzLjT50Y36DCozDWm3zJnu0bUH\nP7fdRirhEKQ1B7dEeWwgQcNsOZmy6XFt81drGh3zmOnKCD5DfTjzE9xHdwIDAQAB\nAoGBAIcrDyHbpWu6FILkiKuo2RgmA3gbBjaZln8sEPpsYU13LDM2K/Mg8CsdFTXZ\n0OiEO1j6Ys+S20RE1SbQ5rf1Maf58bmSVjErALz3GiFddWpF1XDSNEc2dg1aIG+t\niBwtiQAQ7ywlOgm70dwSYEYB0eAyjUybCocfFFZ2tlCVn7ppAkEAwhkwgCRPvC/z\n37R/IQqsAwr2Fp7cfBtxfXIa+n33nTtAGivnGz2Jy/Zq1OVvFMlitIwCEvEULJN+\nxtQB/pk26wJBAOmrK2vUh1LPyIVLbOmWURQpd15AiYT2bLcImq4hJveOo+NP8i/I\nsGmoGEZKPnABr6LSbtDS4O286mj3nCOfJqUCQEDzwvourIwSE+8ZbK1278b45Q7+\nzFOvr1PGWmbWvoTcLgBUDrtb5X/ejzN9L6XqGmDGtW73Q8QC+5q3mY9EYE8CQQDb\ntqZaevlPZa8fnt9m+H9+XMsv5bEpQ+jPZhjDuMqCJi52E/se8S7n+jXxCeiRuxQi\nHooycscq4+LqFkFLwV89AkBsL60YDWplZTTxyXXTmgTxt4JYwH4fQtR+RV9YvCGg\nOw/C9PSCDF2f4vL5BZzQro1DclVTKAlVNYITWBOvVZFH\n-----END RSA PRIVATE KEY-----'
SECUREST_PROTECT_LIST = [
    '/test/',
]