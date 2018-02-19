# -*- coding: utf-8 -*-
"""

"""
import json
from django.http import (HttpResponse)
from django.shortcuts import (render, get_object_or_404, redirect)
from django.core.urlresolvers import (reverse)
from django.views.decorators.csrf import (csrf_exempt)
from django.contrib.auth.decorators import login_required
from django.utils.encoding import (smart_unicode)
from rest_framework import (viewsets)
from rest_framework.response import (Response)
from rest_framework import (status)
from .models import (Anotacion, Documento, Parrafo, Oracion, TAG)
from .forms import DocumentoForm
from .serializers import (OracionSerializer, ParrafoSerializer, TAGLeyesSerializer, AnotacionSerializer)


@login_required
def AnotacionGeneralView(request, anotacion_id):
    """
    :param request:
    :param anotacion_id:
    :return:
    """
    print("AnotacionView")
    print(anotacion_id)
    #import ipdb; ipdb.set_trace()
    #template_name='documentos/generar_anotacion.html'
    template_name='documentos/generar_anotacion_2.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id)
    documento = anotacion.documento

    if request.method == 'POST':
        return render(request, template_name=template_name,
                      context={'anotacion':anotacion,
                               'palabras': json.dumps(json.loads(anotacion.get_texto())[:500]),
                               })

    """
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
    """

    #Retornar el primer Parrafo del documento/anotacion
    #import ipdb; ipdb.set_trace()
    parrafo = documento.get_siguiente_parrafo()
    print("parrafo: {0} ".format(parrafo))
    return redirect(reverse('documentos_app:anotacion-especifica',
                            kwargs={'anotacion_id':anotacion_id, 'parrafo_id':parrafo.id})
                    )
    #kwargs={'anotacion_id':anotacion_id}
    tags_leyes={}
    try:
        #INTENTANDO SACAR LAS TAGS
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).count()
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))

    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           #'palabras': json.loads(parrafo.texto),
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           })


@login_required
def AnotacionView(request, anotacion_id, parrafo_id):
    """
    :param request:
    :param anotacion_id:
    :param parrafo_id:
    :return:
    """
    print("AnotacionView")
    print(anotacion_id, parrafo_id)
    #import ipdb; ipdb.set_trace()
    #template_name='documentos/generar_anotacion.html'
    template_name='documentos/generar_anotacion_2.html'
    anotacion = get_object_or_404(Anotacion, id=anotacion_id, anotador=request.user)
    if anotacion.is_done:
        print("ya se marco como terminada la anotacion, redirijimos a perfil")
        return redirect(reverse('usuarios_app:perfil_home'))

    parrafo = get_object_or_404(Parrafo, id=parrafo_id, documento__id=anotacion.documento.id)
    documento = anotacion.documento


    """
    if request.method == 'POST':
        return render(request, template_name=template_name,
                      context={'anotacion':anotacion,
                               'palabras': json.dumps(json.loads(anotacion.get_texto())[:500]),
                               })

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
    """

    #Retornar el primer Parrafo del documento/anotacion
    #import ipdb; ipdb.set_trace()
    #parrafo = documento.get_siguiente_parrafo()
    print("parrafo: {0} ".format(parrafo))
    tags_leyes={}
    try:
        #INTENTANDO SACAR LAS TAGS
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).count()
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))

    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'get_next_parrafo': parrafo.get_next_parrafo(),
                           'get_prev_parrafo': parrafo.get_prev_parrafo(),
                           #'palabras': json.loads(parrafo.texto),
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'parrafo':parrafo,
                           })


@login_required
def TerminarDocumentoView(request, anotacion_id):
    """
    Retorna el formulario para terminar de agregar los datos del documento
    :param request:
    :param anotacion_id:
    :return:
    """
    print("TerminarDocumentoView")
    #import ipdb; ipdb.set_trace()
    print(anotacion_id)
    documento = get_object_or_404(Documento, id=anotacion_id)
    documento_form = DocumentoForm(instance=documento)
    if 'anotacion_id' in request.session:
        anotacion_id = request.session['anotacion_id']
    # Obtener lista de ID's de de palabras etiquetadas

    return render(request, template_name='documentos/terminar_documento.html',
                  context={'documento':documento,
                           'documento_form':documento_form,
                           'anotacion_id':anotacion_id})


### GUARDAR LA ANOTACION
@csrf_exempt
def guardar_anotacion(request):
    """
    Funcion para gestionar el guardado de anotaciones

    :param request:

    :param id_anotacion: Para identificar que Anotacion se debe guardar
    :param tipo_anotacion: 'texto' o 'palabraas', para saber el tipo de etiquetado
    :param clasificacion: 'texto_jurisprudencia', 'referencia_jurisprudencia'', etc.

    :return:
    """
    if request.method == 'POST':
        print("guardar anotacion")
        print(request.method)
        print(request.POST)
        is_valid=True
        import ipdb; ipdb.set_trace()
        if request.POST:
            informacion = json.loads(json.dumps(request.POST))
        else:
            return HttpResponse("POST vacio")

        if not 'id_anotacion' in informacion:
            is_valid=False
            print("Falta el ID de anotacion")

        if not 'tipo_anotacion' in informacion:
            is_valid=False
            print("Falta el tipo de anotacion")

        if not 'clasificacion' in informacion:
            is_valid=False
            print("Falta la clasificacion de la anotacion")

        if not 'informacion' in informacion:
            is_valid=False
            print("Falta la informacion de la anotacion")
        if is_valid:
            print("PROCESAMOS/ GUARDAMOS LA ANOTACION")
            return HttpResponse("EXITO !! :D")

        return HttpResponse("ERROR, no se envio la informacion completa")
    return HttpResponse("Metodo GET  no permitido")




class OracionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Oracion.objects.all()
    serializer_class = OracionSerializer

    #def create(self, request, *args, **kwargs):
    #    print("METODO CREATE AnotacionViewSet")
    #    import ipdb; ipdb.set_trace()
    #    request = super(OracionViewSet, self).create(request, *args, **kwargs)




    def create(self, request, *args, **kwargs):
        print("METODO CREATE OracionViewSet")
        #import ipdb; ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ParrafoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Parrafo.objects.all()
    serializer_class = ParrafoSerializer

    #def create(self, request, *args, **kwargs):
    #    print("METODO CREATE AnotacionViewSet")
    #    import ipdb; ipdb.set_trace()
    #    request = super(ParrafoViewSet, self).create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print("METODO CREATE ParrafoViewSet")
        #import ipdb; ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        print("update de ParrafoViewSet")
        return super(ParrafoViewSet, self).update(request, *args, **kwargs)



class TAGSLeyesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = TAG.objects.all()
    queryset = TAG.objects.filter(subtag=TAG.objects.get(texto='leyes'))
    serializer_class = TAGLeyesSerializer

    #def create(self, request, *args, **kwargs):
    #    print("METODO CREATE AnotacionViewSet")
    #    import ipdb; ipdb.set_trace()
    #    request = super(ParrafoViewSet, self).create(request, *args, **kwargs)


class AnotacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = TAG.objects.all()
    queryset = Anotacion.objects.all()
    serializer_class = AnotacionSerializer

    def create(self, request, *args, **kwargs):
        print("METODO CREATE AnotacionViewSet")
        import ipdb; ipdb.set_trace()
        request = super(ParrafoViewSet, self).create(request, *args, **kwargs)

