# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

def get_documento_path(instance, filename):
    """
    :param instance:
    :param filename:
    :return:
    """
    return 'documentos/'
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

#@TODO
#Se pueden ordenar los documentos segun la jerarquia que mas convenga
# asunto --> materia -- organo
# organo --> materia -- asunto
# etc.
#   definir csi habra esa especia de ordenamiento, o todos van al mismo lugar


class Documento(models.Model):
    """  """

    tipo_asunto = models.CharField(max_length=60, blank=True,
                                null=True, default="")
    materia = models.CharField(max_length=60, blank=True,
                                null=True, default="")
    organo_jurisdiccional = models.CharField(max_length=60, blank=True,
                                null=True, default="")

    texto_html = models.CharField(max_length=60, blank=True,
                                  null=True, default="")

    archivo = models.FileField(upload_to=get_documento_path)


class Anotacion(models.Model):
    """  """

    documento = models.ForeignKey(Documento,
                                related_name='anotacion')
    revisor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='revisor')

    anotador = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='anotador')


class TAG(models.Model):
    """  """

    texto = models.CharField(max_length=60, blank=True,
                             null=True, default="")


class Oracion(object):
    """  """
    tag = models.ForeignKey(TAG, related_name='tag')

    texto = models.CharField(max_length=60, blank=True,
                             null=True, default="")

    evaluado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='etiquetador')


class EstadoEtiquetado(object):
    """  """
    pass





