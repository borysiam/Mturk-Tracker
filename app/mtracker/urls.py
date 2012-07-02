from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('mtracker',

    #url(r'^$', 'main.views.index', name='index'),

    url(r'^admin/', include(admin.site.urls)),

    (r'^bad/$', bad),
)

urlpatterns += patterns('',
    url(r'^api/', include('mturk.api.urls')),
    url('', include('mturk.main.urls')),
    url(r'^docs/', include('sphinxdoc.urls')),
    url(r'^search/', include('haystack.urls')),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
