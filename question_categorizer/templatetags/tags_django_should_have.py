from django import template

register = template.Library()

@register.filter(name="in")
def inside(value, arg):
    arg = map(lambda element: int(element.encode('utf-8')), arg)
    return value in arg 

@register.filter(name="id")
def get_id(value):
    return value.id
