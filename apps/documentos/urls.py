# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (AnotacionGeneralView, AnotacionView, TerminarDocumentoView,
                    guardar_anotacion, OracionViewSet, ParrafoViewSet,
                    TAGSLeyesViewSet, AnotacionViewSet)


guardar_anotacion = OracionViewSet.as_view({'post':'create'})
terminar_parrafo = ParrafoViewSet.as_view({'patch':'update'})

terminar_anotacion = AnotacionViewSet.as_view({'patch':'update'})
listado_leyes = TAGSLeyesViewSet.as_view({'get':'list'})

documentos_urls = [
    url(r'^anotacion/(?P<anotacion_id>\d+)$', AnotacionGeneralView, name='anotacion-general'),
    url(r'^anotacion/(?P<anotacion_id>\d+)/parrafo/(?P<parrafo_id>\d+)$', AnotacionView, name='anotacion-especifica'),
    url(r'^anotacion/(?P<id>\d+)/complete$', TerminarDocumentoView, name='terminar_documento'),
    url(r'^anotacion/(?P<pk>\d+)/terminar$', terminar_anotacion, name='terminar_anotacion'),

    url(r'^guardar-anotacion', guardar_anotacion, name='guardar-anotacion'),
    url(r'^parrafo/(?P<pk>\d+)', terminar_parrafo, name='terminar_parrafo'),
    url(r'^lista-leyes', listado_leyes, name='lista-leyes'),

]


