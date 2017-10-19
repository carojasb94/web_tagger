
from django.conf.urls import url
from django.contrib import admin

from views import (home, do_login, do_logout)

registro_urls = [
    url(r'^$', home),
    url(r'^login$', do_login, name='login'),
    url(r'logout', do_logout, name='logout'),
]
