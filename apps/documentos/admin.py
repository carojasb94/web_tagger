# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import (Documento, Anotacion,
                     TAG, Oracion, EstadoEtiquetado, Clasificacion)


class DocumentoInline(admin.TabularInline):
    model = Documento

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        print("get queryset")
        print(self)
        print(request)
        qs = super(DocumentoInline, self).get_queryset(request)
        print(qs)
        return qs.none()


class DocumentoAdmin(admin.ModelAdmin):
    pass


class AnotacionAdmin(admin.ModelAdmin):
    pass


class ClasificacionAdmin(admin.ModelAdmin):
    pass


class TAGAdmin(admin.ModelAdmin):
    pass


class OracionAdmin(admin.ModelAdmin):
    pass


#class EstadoEtiquetadoAdmin(admin.ModelAdmin):
#    pass


admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Anotacion, AnotacionAdmin)
#admin.site.register(Oracion, OracionAdmin)
admin.site.register(TAG, TAGAdmin)
admin.site.register(Clasificacion, ClasificacionAdmin)

#admin.site.register(EstadoEtiquetado, EstadoEtiquetadoAdmin)

