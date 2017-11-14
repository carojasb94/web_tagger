# -*- coding: utf-8 -*-
from django.shortcuts import render


def PerfilView(request):
    print("Home del Usuario anotador")
    return render(request, template_name='usuarios/perfil.html',
                  context={})


def AnotadorView(request):
    print("Home del Usuario anotador")
    return render(request, template_name='usuarios/anotador.html',
                  context={})


def RevisorView(request):
    print("Home del Usuario revisor")
    return render(request, template_name='usuarios/revisor.html',
                  context={})
