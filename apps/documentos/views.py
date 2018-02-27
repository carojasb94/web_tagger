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
from .models import (Anotacion, Documento, Parrafo, Oracion, TAG,
                     EvaluacionParrafo, Clasificacion, TAGPersonal,
                     ArgumentacionParrafo)
from .forms import DocumentoForm
from .serializers import (OracionSerializer, ParrafoSerializer,
                          TAGLeyesSerializer, AnotacionSerializer,
                          ArgumentacionParrafoSerializer)


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
        tags_leyes = TAG.objects.filter(subtag=TAG.objects.get(texto="leyes")).values('id','texto')
        #print("tag leyes: ")
        #print(tags_leyes)
    except Exception as e:
        print("error al intentar obtener tags de leyes: {0}".format(e))

    #Validar argumentacion del parrafo
    has_argumentacion=False
    if (ArgumentacionParrafo.objects.filter(autor=request.user, parrafo=parrafo).exists()):
        print("ya tiene argumentacion el parrafo")
        has_argumentacion=True


    return render(request, template_name=template_name,
                  context={'anotacion':anotacion,
                           'get_next_parrafo': parrafo.get_next_parrafo(),
                           'get_prev_parrafo': parrafo.get_prev_parrafo(),
                           #'palabras': json.loads(parrafo.texto),
                           'palabras': parrafo.texto,
                           'parrafo_id':parrafo.id,
                           'tags_leyes':tags_leyes,
                           'parrafo':parrafo,
                           'has_argumentacion':has_argumentacion,
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
        print("funcion guardar_anotacion")
        print("Validando que venga request.POST")
        print(request.method, request.POST)

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
        clasificacion = ""
        informacion_tags = {}
        if request.data.get('clasificacion', False):
            print(request.data['clasificacion'])
            clasificacion = request.data['clasificacion']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        oracion = serializer.instance

        #if


        ## Generamos el historial (EvaluacionParrafo)


        #Considerando el caso de etiquetado de referenfia a articulo
        if clasificacion == 'referencia_articulo':
            #import ipdb; ipdb.set_trace()
            print("Anotacion de referencia a articulo")
            #Obtenemos las etiquetas enviadas
            print(oracion)
            tag_ley = request.data.get("tag_ley", "")
            tag_numero_articulo = request.data.get("tag_numero_articulo", "")
            tag_apartado = request.data.get("tag_apartado", "")
            tag_fraccion = request.data.get("tag_fraccion", "")
            tag_inciso = request.data.get("tag_inciso", "")
            tag_parrafo = request.data.get("tag_parrafo", "")

            #Obteniendo clasificacion
            custom_classificacion = Clasificacion.objects.get(key='creada_por_usuario')

            if tag_numero_articulo:
                #tag_numero_articulo = TAG.objects.get(texto='numero_articulo')
                #Creando tag numero_articulo
                tna, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='numero_articulo'), texto=tag_numero_articulo)
                oracion.tags.add(tna)
                TAGPersonal.objects.get_or_create(tag=tna, alias='default')

            if tag_apartado:
                #tag_apartado = TAG.objects.get(texto='apartado')
                #Creando tag numero_articulo
                ta, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='apartado'), texto=tag_apartado)
                oracion.tags.add(ta)
                TAGPersonal.objects.get_or_create(tag=ta, alias='default')

            if tag_fraccion:
                #tag_fraccion = TAG.objects.get(texto='fraccion')
                #Creando tag numero_articulo
                tf, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='fraccion'), texto=tag_fraccion)
                oracion.tags.add(tf)
                TAGPersonal.objects.get_or_create(tag=tf, alias='default')
            if tag_inciso:
                #tag_inciso = TAG.objects.get(texto='inciso')
                #Creando tag numero_articulo
                ti, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='inciso'), texto=tag_inciso)
                oracion.tags.add(ti)
                TAGPersonal.objects.get_or_create(tag=ti, alias='default')

            if tag_parrafo:
                #tag_parrafo = TAG.objects.get(texto='parrafo')
                #Creando tag numero_articulo
                tp, creado = TAG.objects.get_or_create(subtag=TAG.objects.get(texto='parrafo'), texto=tag_parrafo)
                oracion.tags.add(tp)
                TAGPersonal.objects.get_or_create(tag=tp, alias='default')
            oracion.save()



        # Se genera el historial de la anotacion

        self.generar_evaluacion_parrafo(request, oracion)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def generar_evaluacion_parrafo(self, request, oracion):
        """
        Funcion para generar el historial de modificaciones de una oracion
        """
        evaluacion = EvaluacionParrafo.objects.create(
            autor=request.user,oracion=oracion, texto=oracion.texto,
            tipo_anotacion=oracion.tipo_anotacion,
            clasificacion=oracion.clasificacion,
        )

        if oracion.tags.all():
            evaluacion.tags.add(*oracion.tags.all())
        #evaluacion.save()



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

    def guardar_argumentacion(self, request, *args, **kwargs):
        print("guardar_argumentacion de ParrafoViewSet")
        import ipdb; ipdb.set_trace()
        argumentacion = ArgumentacionParrafoSerializer(data=request.POST, context={'request':request})
        if argumentacion.is_valid():
            print("argumentacion valida")
            print(argumentacion.validated_data)
            # validar que el usuario sea propietario del parrafo evaluado
            argumentacion.save()

        return super(ParrafoViewSet, self).update(request, *args, **kwargs)



class TAGSLeyesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TAG.objects.all()
    #queryset = TAG.objects.filter(subtag=TAG.objects.get(texto='leyes'))
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
        request = super(AnotacionViewSet, self).create(request, *args, **kwargs)



class ArgumentacionParrafoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = TAG.objects.all()
    queryset = ArgumentacionParrafo.objects.all()
    serializer_class = ArgumentacionParrafoSerializer

    def create(self, request, *args, **kwargs):
        print("METODO CREATE ArgumentacionParrafo")
        import ipdb; ipdb.set_trace()
        request = super(ArgumentacionParrafoViewSet, self).create(request, *args, **kwargs)
        return request



