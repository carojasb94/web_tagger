# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (AnotacionView)


documentos_urls = [
    url(r'^anotacion/(?P<id>\d+)/$', AnotacionView, name='crear_anotacion'),
]


