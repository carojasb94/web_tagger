# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Anotacion

# Create your views here.


def AnotacionView(request, id):
    print("AnotacionView")
    print(id)
    anotacion = get_object_or_404(Anotacion, id=id)


    return render(request, template_name='documentos/generar_anotacion.html',
                  context={'anotacion':anotacion})
