# -*- coding: utf-8 -*-


from django.contrib.auth.models import User, Group
from django.shortcuts import (get_object_or_404)
from rest_framework import serializers
from .models import (Anotacion, Oracion, Parrafo, TAG, Clasificacion, ArgumentacionParrafo)


class OracionSerializer(serializers.ModelSerializer):
    """ """

    clasificacion = serializers.CharField()
    texto = serializers.CharField(required=True)

    class Meta:
        model = Oracion
        fields = ('anotacion', 'parrafo', 'evaluado_por', 'tipo_anotacion', 'texto', 'clasificacion')

    def create(self, validated_data):
        print("metodo create en serializer de oracionserializer")
        print(validated_data)
        #import ipdb; ipdb.set_trace()
        clasificacion = get_object_or_404(Clasificacion, key=validated_data['clasificacion'])
        validated_data['clasificacion'] = clasificacion
        return super(OracionSerializer, self).create(validated_data, )





class ParrafoSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Parrafo
        fields = ('id', 'ha_sido_evaluado')


class TAGLeyesSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = TAG
        fields = ('id', 'texto')



class AnotacionSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Anotacion
        fields = ('is_done',)


from rest_framework.fields import CurrentUserDefault

class ArgumentacionParrafoSerializer(serializers.ModelSerializer):
    """ """

    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ArgumentacionParrafo
        fields = ('autor', 'parrafo', 'calificacion')

    """
    def save(self):
        print("metodo save de ArgumentacionParrafoSerializer")
        import ipdb; ipdb.set_trace()
        autor = CurrentUserDefault()  # <= magic!
        #title = self.validated_data['title']
        #article = self.validated_data['article']
        return super(ArgumentacionParrafoSerializer, self).save()
        #request = super(ArgumentacionParrafoViewSet, self).create(request, *args, **kwargs)
    """
