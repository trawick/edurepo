from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from resources.models import Resource
from resources.forms import ResourceForm


def index(request):
    resource_list = Resource.objects.order_by('id')
    context = RequestContext(request, {'resource_list': resource_list})
    return render(request, 'resources/index.html', context)


def detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    context = RequestContext(request, {'resource': resource})
    return render(request, 'resources/resource.html', context)


@login_required
def create_resource(request):
    if request.POST:
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/resources')
    else:
        if request.GET and 'objective' in request.GET:
            initial = {'objective': request.GET['objective']}
        else:
            initial = {}
        form = ResourceForm(initial=initial)

    args = {}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'resources/create_resource.html', args)
