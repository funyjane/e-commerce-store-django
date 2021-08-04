from django import template

register = template.Library()
register.simple_tag(lambda x: x[::-1], name="reverse_string")
