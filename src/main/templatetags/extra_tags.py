from django import template

register = template.Library()

register.simple_tag(lambda x: x[::-1], name="reverse_string")


@register.filter(name="get_fields")
def get_fields(obj):

    """Returns all fields for the model object"""

    return [
        (obj.__class__._meta.get_field(x.name).verbose_name, getattr(obj, x.name))
        for x in obj.__class__._meta.local_fields
    ]
