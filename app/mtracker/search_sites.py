"""This file is required by haystack of version < 2.0.
2.0 is in beta stage and django-sphinxdoc does not have full support.

Include the following in settings:

HAYSTACK_SITECONF = "mtracker.search_sites"

"""
import search_indexes
import haystack
haystack.autodiscover()
