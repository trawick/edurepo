from django import template

register = template.Library()


def dereference(value, arg):
    print value
    print arg
    return value[arg]


register.filter('dereference', dereference)
