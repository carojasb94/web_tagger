# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin

from .views import (PerfilView, AnotadorView, RevisorView)

usuarios_urls = [
    url(r'^perfil$', PerfilView, name='perfil_home'),
    url(r'^anotador$', AnotadorView, name='anotador_home'),
    url(r'^revisor$', RevisorView, name='revisor_home'),
]
