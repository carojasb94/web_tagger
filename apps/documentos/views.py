# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from .models import (Anotacion, Documento)
from .forms import DocumentoForm


def AnotacionView(request, id):
    print("AnotacionView")
    print(id)
    #import ipdb; ipdb.set_trace()
    anotacion = get_object_or_404(Anotacion, id=id)
    documento = anotacion.documento
    if request.method == 'POST':
        return render(request, template_name='documentos/generar_anotacion.html',
                      context={'anotacion':anotacion})

    if ((not documento.juez) or (not documento.secretario) or (not documento.preambulo)
        or (not documento.resultandos) or (not documento.considerandos)
        or (not documento.puntos_resolutivos)):
        #En caso de que algun campo este vacio, se redirige la peticion a complementar
        # la informacion
        print("Terminar de llenar la informacion del documento")
        anotacion_id = id
        request.session['anotacion_id'] = id
        return redirect(reverse('documentos_app:terminar_documento',kwargs={'id':documento.id}),
                        kwargs={'anotacion_id':anotacion_id}
                        )
    return render(request, template_name='documentos/generar_anotacion.html',
                  context={'anotacion':anotacion})


def TerminarDocumentoView(request, id):
    """
    Retorna el formulario para terminar de agregar los datos del documento
    :param request:
    :param id:
    :return:
    """
    print("TerminarDocumentoView")
    #import ipdb; ipdb.set_trace()
    print(id)
    documento = get_object_or_404(Documento, id=id)
    documento_form = DocumentoForm(instance=documento)
    if 'anotacion_id' in request.session:
        anotacion_id = request.session['anotacion_id']
    return render(request, template_name='documentos/terminar_documento.html',
                  context={'documento':documento,
                           'documento_form':documento_form,
                           'anotacion_id':anotacion_id})
