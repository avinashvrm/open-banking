from django_hosts import patterns, host
from django.contrib import admin
from . import admin_urls

host_patterns = patterns('',
    host(r'www', 'openbanking.urls', name='www'),
    host(r'admin', admin_urls, name='admin'),
)