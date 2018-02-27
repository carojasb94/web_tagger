# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import (Documento, Anotacion,
                     TAG, Oracion, EstadoEtiquetado, Clasificacion,
                     Parrafo, DummyParrafo, EvaluacionParrafo,
                     TAGPersonal, ArgumentacionParrafo)


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


class ParrafoAdmin(admin.ModelAdmin):
    pass

class OracionAdmin(admin.ModelAdmin):
    pass


class DummyAdmin(admin.ModelAdmin):
    pass


class EvaluacionParrafoAdmin(admin.ModelAdmin):
    pass

class TAGPersonalAdmin(admin.ModelAdmin):
    pass

class ArgumentacionParrafoAdmin(admin.ModelAdmin):
    pass


#class EstadoEtiquetadoAdmin(admin.ModelAdmin):
#    pass


admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Anotacion, AnotacionAdmin)
#admin.site.register(Oracion, OracionAdmin)
admin.site.register(TAG, TAGAdmin)
admin.site.register(Clasificacion, ClasificacionAdmin)

admin.site.register(Parrafo, ParrafoAdmin)
admin.site.register(Oracion, OracionAdmin)
admin.site.register(DummyParrafo, DummyAdmin)
admin.site.register(EvaluacionParrafo, EvaluacionParrafoAdmin)
admin.site.register(TAGPersonal, TAGPersonalAdmin)


admin.site.register(ArgumentacionParrafo, ArgumentacionParrafoAdmin)



#admin.site.register(EstadoEtiquetado, EstadoEtiquetadoAdmin)

