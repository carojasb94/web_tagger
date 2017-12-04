# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import (Documento)

class DocumentoForm(ModelForm):
    class Meta:
        model = Documento
        fields = ['juez', 'secretario', 'preambulo',
                  'resultandos', 'considerandos', 'puntos_resolutivos']

        labels = {
                    'juez': _('Writer'),
                }
        error_messages = {
            'juez': {
                'max_length': _("This writer's name is too long."),
            },
                }
