# -*- coding: utf-8 -*-
"""
"""
from .models import Clasificacion

def say_hello(request):
    print("say_hello")
    print(request)
    #import ipdb;ipdb.set_trace();
    if request.user.is_authenticated():
        print("esta logeado")

    return {'say_hello':"Hello",}


def context_processors_anotaciones(request):
    print("context_processors_anotaciones")
    print(request)
    #import ipdb;ipdb.set_trace();
    if request.user.is_authenticated():
        print("esta logeado")
        anotaciones_pendientes = request.user.anotador.filter(is_done=False)
        revisiones_pendientes = request.user.revisor.filter(is_done=False)
        return {'anotaciones_pendientes': anotaciones_pendientes,
                'revisiones_pendientes':revisiones_pendientes,
                'clasificaciones':Clasificacion.objects.all().exclude(key='creada_por_usuario')
                }
    return {}


