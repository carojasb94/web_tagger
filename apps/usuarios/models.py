# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    #user = models.ForeignKey(related_name='user')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='perfil')
    nombres = models.CharField(max_length=60, blank=True,
                                null=True, default="")
    apellidos = models.CharField(max_length=60, blank=True,
                                  null=True, default="")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_usuario(sender, **kwargs):
    #print("crear_usuario (signal)!")
    #Si existe la instancia, no creamos relacion
    if kwargs['instance'].id:
        try:
            if not Perfil.objects.filter(user=kwargs['instance']).exists():
                print("USUARIO NUEVO, creamos relacion Perfil")
                Perfil.objects.create(user=kwargs['instance'])
        except Exception as e:
            print(e)
    else:
        print("Fue actualizacion del modelo, ignoramos")

