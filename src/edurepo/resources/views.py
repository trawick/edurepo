from django.shortcuts import render
from django.template import RequestContext
from resources.models import Resource


def index(request):
    resource_list = Resource.objects.order_by('id')
    context = RequestContext(request, {'resource_list': resource_list})
    return render(request, 'resources/index.html', context)


def detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    context = RequestContext(request, {'resource': resource})
    return render(request, 'resources/resource.html', context)
