from django import template

register = template.Library()


def dereference(value, arg):
    return value[arg]


register.filter('dereference', dereference)
