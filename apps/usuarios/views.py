# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def PerfilView(request):
    print("Home del Usuario anotador")
    anotaciones_pendientes = list()

    return render(request, template_name='usuarios/perfil.html',
                  context={})


@login_required
def AnotadorView(request):
    print("Home del Usuario anotador")
    return render(request, template_name='usuarios/anotador.html',
                  context={})


@login_required
def RevisorView(request):
    print("Home del Usuario revisor")
    return render(request, template_name='usuarios/revisor.html',
                  context={})



