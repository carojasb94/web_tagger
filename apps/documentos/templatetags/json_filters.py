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


def jsonify_leyes(object):
    """
    :param object:
    :return:
    """
    return mark_safe(simplejson.dumps([o for o in object]))


register.filter('jsonify', jsonify)
register.filter('jsonify_leyes', jsonify_leyes)
jsonify.is_safe = True
jsonify_leyes.is_safe = True

