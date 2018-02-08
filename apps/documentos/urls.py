# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (AnotacionView, TerminarDocumentoView,
                    guardar_anotacion, OracionViewSet, ParrafoViewSet)

guardar_anotacion = OracionViewSet.as_view({'post':'create'})
terminar_parrafo = ParrafoViewSet.as_view({'patch':'update'})

documentos_urls = [
    url(r'^anotacion/(?P<id>\d+)/$', AnotacionView, name='crear_anotacion'),
    url(r'^anotacion/documento/(?P<id>\d+)/$', TerminarDocumentoView, name='terminar_documento'),
    url(r'^guardar-anotacion', guardar_anotacion, name='terminar_documento'),
    url(r'^parrafo/(?P<pk>\d+)', terminar_parrafo, name='terminar_parrafo'),
]


