# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import logging
import subprocess
from django.db import models
from django.conf import settings

from utils.funciones import (acomodaTexto, marcarConsiderandos,
                             limpiarTexto, restaurarNumeros,
                             convertir_texto_a_bd, dar_formato_a_texto)

from django.contrib.postgres import fields

logger = logging.getLogger('modelos')

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

    texto_html = models.TextField(max_length=300000, blank=True,
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

    def crear_parrafo(self, numero_inicial, numero_final, parrafo_actual):
        Parrafo.objects.create(documento=self, numero_inicial=numero_inicial,
                               numero_final=numero_final,texto=parrafo_actual,
                               tipo='inicio')
        try:
            DummyParrafo.objects.create(
                texto={'1':'hola',
                       '2':'nanoz'}
            )
        except Exception as e:
            print("fallo tercero dummy ")
            print(e)




    def get_siguiente_parrafo(self):
        return self.parrafo.exclude(ha_sido_evaluado=True).first()

    def get_dummy_parrafo(self):
        return DummyParrafo.objects.first()


class Parrafo(models.Model):
    """
    Clase para guardar los parrafos encontrados en el Documento
    """
    documento = models.ForeignKey(Documento, related_name='parrafo')

    numero_inicial=models.IntegerField(blank=True, null=True,
        help_text="Indice de inicio delas palabras")

    numero_final = models.IntegerField(blank=True, null=True,
        help_text="Indice de inicio delas palabras")

    texto = fields.JSONField()

    ha_sido_evaluado = models.BooleanField(
        help_text='Marcar cuando un parrafo ya ha sido evaluado',
        default=False)

    tipo = models.CharField(
        help_text="Saber si es considerando, resultando, resuelve, etc.",
        max_length=40, blank=True, null=True)

    def __str__(self):
        return "{0}: {1} {2}".format(self.id, self.numero_inicial, self.numero_final)




class DummyParrafo(models.Model):
    """"""

    texto = fields.JSONField()



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

    #def get_texto(self):
    #    return json.loads(self.documento.texto_html)

    def get_texto(self):
        return self.documento.texto_html

    def set_texto(self, texto):
        self.documento.texto_html = texto
        #self.documento.texto_html = json.dumps(texto)

    def save_documento(self):
        self.documento.save()


class Clasificacion(models.Model):
    """ """

    texto = models.CharField(max_length=60, blank=True,
                             null=True, default="")

    def __str__(self):
        return "{0}".format(self.texto)


class TAG(models.Model):
    """  """

    texto = models.CharField(max_length=1000, blank=True,
                             null=True, default="")

    clasificacion = models.ForeignKey(Clasificacion)
    is_active = models.BooleanField(default=True)
    subtag = models.ForeignKey('self', blank=True, null=True)


    def __str__(self):
        return "{0}".format(self.texto).encode('utf-8')

    #def __unicode__(self):
    #    return "{0}".format(self.texto).decode('utf-8')


class Oracion(models.Model):
    """  """
    tags = models.ForeignKey(TAG, related_name='tags', null=True, blank=True)

    anotacion = models.ForeignKey(Anotacion, related_name='oraciones')
    parrafo = models.ForeignKey(Parrafo, related_name='oraciones')

    tipo_anotacion = models.CharField(max_length=100, blank=True,
                                      null=True, default="")

    texto = models.CharField(max_length=2000, blank=True,
                             null=True, default="")

    evaluado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='etiquetador')

    is_correcta = models.BooleanField(default=True)

    def __str__(self):
        return "Oracion {0}".format(self.id)

    def __unicode__(self):
        return u"Oracion {0}".format(self.id)


class EstadoEtiquetado(object):
    """  """
    pass





###################### DEFINIENDO SIGNALS
from django.db.models.signals import (post_save, pre_save)
from django.dispatch import receiver


@receiver(post_save, sender=Documento)
def crear_ticket_cepra(sender, **kwargs):
    #import ipdb; ipdb.set_trace()
    if kwargs['created']:
        #EJECUTAMOS LA LECTURA Y GUARDADO DE LA INFORMACION DEL ARCHIVO PDF
        logger.debug("Documento guardado, procedemos a guardar informacion")
        #import ipdb; ipdb.set_trace()

        filepath =  kwargs['instance'].get_path()
        _path_ = filepath.split('/')
        print(os.getcwd())
        root_path = os.getcwd() + "/".join(_path_[:len(_path_)-1])

        filepath_prov = os.path.join(root_path, _path_[-1].
                                     replace('.PDF','.txt').replace('.pdf','.txt'))
        print("PATHS: ")
        print(filepath)
        print(_path_)
        print(filepath_prov)
        command = ["pdftotext", "-layout", "-raw", "-q",
                   os.getcwd()+filepath, filepath_prov
                   ]

        print(" ".join(command))
        proceso = subprocess.Popen(command, stdout=subprocess.PIPE)
        exit_code = proceso.wait()
        print(exit_code)

        ## GREGANDO SCRIPT QUE DA FORMATO AL ARCHIVO EXTRAIDO CON PDFTOTEXT
        texto = dar_formato_a_texto(filepath_prov, new_path=None)
        print("termino de dar formato...")

        # Interpretar el texto formateado
        all_words = convertir_texto_a_bd(texto, kwargs['instance'])

        #anotacion.set_texto(json.dumps(['ESTO','es','una','lista','de','palabras','alv',':v']))
        #Guardar la conversion final del texto en la bd
        #kwargs['instance'].texto_html = json.dumps(all_words)
        #kwargs['instance'].save()

    else:
        pass
