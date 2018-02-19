# -*- coding: utf-8 -*-


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (Anotacion, Oracion, Parrafo, TAG)


class OracionSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Oracion
        fields = ('anotacion', 'parrafo', 'evaluado_por', 'tipo_anotacion', 'texto')


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

