# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (AnotacionView, TerminarDocumentoView)


documentos_urls = [
    url(r'^anotacion/(?P<id>\d+)/$', AnotacionView, name='crear_anotacion'),
    url(r'^anotacion/documento/(?P<id>\d+)/$', TerminarDocumentoView, name='terminar_documento'),
]


