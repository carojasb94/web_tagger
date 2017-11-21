# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from django.conf import settings

def get_documento_path(instance, filename):
    """
    :param instance:
    :param filename:
    :return:
    """
    return 'documentos/{0}'.format(filename)
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

    juez = models.CharField(max_length=80, blank=True,
                            null=True, default="")
    secretario = models.CharField(max_length=80, blank=True,
                                  null=True, default="")
    preambulo = models.CharField(max_length=80, blank=True,
                                 null=True, default="")
    resultandos = models.CharField(max_length=80, blank=True,
                                   null=True, default="")
    considerandos = models.CharField(max_length=80, blank=True,
                                     null=True, default="")
    puntos_resolutivos = models.CharField(max_length=80, blank=True,
                                          null=True, default="")
    #url = models.SlugField(max_length=80, blank=True,
    #                       null=True)

    def __str__(self):
        return "Documento {0} - {1}".format(self.id, self.archivo)

    def get_path(self):
        return self.archivo.url


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

    is_done = models.BooleanField(default=False)

    def __str__(self):
        return "Anotacion {0} - {1}".format(self.id, self.documento)

    def get_url_file(self):
        return self.documento.get_path()

    def get_texto(self):
        return json.loads(self.documento.texto_html)

    def set_texto(self, texto):
        self.documento.texto_html = json.dumps(texto)

    def save_documento(self):
        self.documento.save()

class TAG(models.Model):
    """  """

    texto = models.CharField(max_length=60, blank=True,
                             null=True, default="")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{0}".format(self.texto)

class Oracion(object):
    """  """
    tag = models.ForeignKey(TAG, related_name='tag')

    texto = models.CharField(max_length=500, blank=True,
                             null=True, default="")

    evaluado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='etiquetador')

    is_correcta = models.BooleanField(default=True)

    def __str__(self):
        return "Oracion {0}".format(self.texto)

class EstadoEtiquetado(object):
    """  """
    pass





