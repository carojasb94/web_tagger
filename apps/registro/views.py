# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect #, reverse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView


def home(request):
    print("home request")

    if request.user.is_authenticated():
        #import ipdb; ipdb.set_trace()
        print("el usuario esta autenticado")
        #return redirect(reverse('home_app:home-page'))

        #@todo validar si es anotador o revisor
        return redirect(reverse('usuarios_app:perfil_home'))

    return redirect(reverse('registro_app:login'))
    #return render(request, template_name='home.html', context={})


def do_login(request):
    """
    :param request:
    :return:
    """
    template_name = "login.html"

    print("do_login request")
    if request.user.is_authenticated():
        #import ipdb; ipdb.set_trace()
        print("el usuario esta autenticado")
        #return redirect(reverse('home_app:home-page'))

        #@todo validar si es anotador o revisor
        return redirect(reverse('usuarios_app:perfil_home'))

    if request.method == 'GET':
        return render(request, template_name, context={})
    elif request.method == 'POST':
        print('metodo post')
        usuario = authenticate(username=request.POST.get('username', ''),
                               password=request.POST.get('password', ''))
        if usuario:
            login(request, usuario)
            print("login correcto")
            #return render(request, template_name, context={'success':'Sin errores'})
            return redirect(reverse('usuarios_app:perfil_home'))
        else:
            return render(request, template_name,
                          context={'error':'Las claves proporcionadas son incorrectas'})
    return render(request, template_name=template_name,
                  context={})


def do_logout(request):
    print("do_logout request")
    logout(request)
    return redirect(reverse('registro_app:home'))


