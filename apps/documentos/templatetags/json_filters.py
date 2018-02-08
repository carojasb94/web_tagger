from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
from django.utils.safestring import mark_safe
try:
    from django.utils import simplejson
except Exception as e:
    import json as simplejson

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

register.filter('jsonify', jsonify)

jsonify.is_safe = True