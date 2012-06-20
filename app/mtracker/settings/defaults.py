import os
import tempfile

DEBUG = True
TEMPLATE_DEBUG = DEBUG
JS_DEBUG = DEBUG

_tempdir = tempfile.tempdir or '/tmp'
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(PROJECT_PATH)))
RUN_DATA_PATH = '/tmp/mturktracker/data'

ADMINS = ()
MANAGERS = ADMINS
DATABASES = {}

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
ugettext = lambda x: x
LANGUAGES = (
  ('en', ugettext('English')),
)
LOCALE_PATHS = ()
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(ROOT_PATH, 'collected_static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',

    'mturk.tabs_context_processor.tabs'
)

ROOT_URLCONF = 'mtracker.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mtracker.wsgi.application'

TEMPLATE_DIRS = (
    "templates",
    os.path.join(ROOT_PATH, 'templates'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(_tempdir, 'mtracker__file_based_cache'),
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

FOREIGN_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.webdesign',

    'haystack',
    'pipeline',
    'south',
    'bootstrap',
    'sphinxdoc',
)

MTRACKER_APPS = (
    'mturk',
    'mturk.main',
    'mturk.importer',
    'mturk.spam',
)

INSTALLED_APPS = tuple(list(FOREIGN_APPS) + list(MTRACKER_APPS))

SOUTH_TESTS_MIGRATE = False

from logging.handlers import SysLogHandler
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (' mturk-tracker: %(name)s %(levelname)s '
                '%(funcName)s:%(lineno)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
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
        },
        'syslog': {
            'level': 'WARNING',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address': '/dev/log',
            'facility': SysLogHandler.LOG_LOCAL2,
        },
        'log_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            # Override this in local settings
            'filename': os.path.join(ROOT_PATH, 'main.log'),
            'maxBytes': '16777216',  # 16megabytes
            'formatter': 'verbose'
        },
        'crawl_log': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            # Override this in local settings
            'filename': os.path.join(ROOT_PATH, 'crawl.log'),
            'maxBytes': '16777216',  # 16megabytes
            'formatter': 'verbose'
        }
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.handlers.SentryHandler',
        # },
    },
    'root': {
        'handlers': ['syslog', ],  # 'sentry'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mturk.main.management.commands': {
            'handlers': ['crawl_log'],
            'level': LOG_LEVEL,
            'propagate': True,
        }
    },
}

PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'less/bootstrap/bootstrap.less',
        ),
        'output_filename': 'css/bootstrap.css',
        'extra_context': {
            'rel': 'stylesheet/less',
        },
    },
    'bootstrap-responsive': {
        'source_filenames': (
            'less/bootstrap/responsive.less',
        ),
        'output_filename': 'css/bootstrap-responsive.css',
        'extra_context': {
            'rel': 'stylesheet/less',
        },
    },

}

PIPELINE_JS = {
    'core': {
        'source_filenames': (
            'js/jquery-1.7.2.js',
            'js/ejs.js',
            'js/view.js',
            'js/underscore.js',
            'js/json2.js',
            'js/backbone.js',
            'js/bootstrap.js',
        ),
        'output_filename': 'js/core.min.js',
    },
    'less': {
        'source_filenames': (
            'js/less-1.3.0.js',
        ),
        'output_filename': 'js/less.min.js',
    },
}

PIPELINE = not DEBUG
if PIPELINE:
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_LESS_BINARY = "lessc"
PIPELINE_YUI_BINARY = os.path.join(ROOT_PATH, 'bin', 'yuicompressor.sh')
PIPELINE_COFFEE_SCRIPT_BINARY = os.path.join(ROOT_PATH, 'bin', 'coffeefinder.sh')

PIPELINE_TEMPLATE_FUNC = 'new EJS'
PIPELINE_TEMPLATE_NAMESPACE = 'window.Template'
PIPELINE_TEMPLATE_EXT = '.ejs'

# do not cache search API results
USE_CACHE = False

API_CACHE_TIMEOUT = 60 * 60 * 24
DYNAMIC_MEDIA = 'd/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

RUN_DATA_PATH = '/tmp'


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
INTERNAL_IPS = ['127.0.0.1']

GOOGLE_ANALYTICS_ID = 'UA-89122-17'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGIN_REDIRECT_URL = "/"

DATASMOOTHING = True

PREDICTION_API_CLIENT_ID = "1096089602663-erfn2lj26ae9n1djidfu8gf2e5egs5bk.apps.googleusercontent.com"
PREDICTION_API_CLIENT_SECRET = "cWPdUE0BCcQsbZZ_xvLO9dMI"

PREDICTION_API_DATA_SET = "mturk-tracker/spam-training-data-20110506.txt"


MTURK_AUTH_EMAIL = None
MTURK_AUTH_PASSWORD = None

HAYSTACK_SITECONF = "mtracker.search_sites"
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'
