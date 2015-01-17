from django.core.context_processors import csrf
from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from edurepo import settings
from resources.models import Resource, ResourceSubmission, ResourceVerification
from resources.forms import ResourceForm, ResourceSubmissionForm
from teachers.views import get_dashboard_emails


def index(request):
    resource_list = Resource.objects.order_by('id')
    return render(request, 'resources/index.html', {
        'resource_list': resource_list,
        'dashboard_emails': get_dashboard_emails(request)
    })


def detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    try:
        rv = ResourceVerification.objects.get(url=resource.url)
    except ResourceVerification.DoesNotExist:
        rv = None
    comments = ResourceSubmission.objects.filter(resource=resource).exclude(comment='')
    return render(request, 'resources/resource.html', {
        'resource': resource,
        'comments': comments,
        'verification': rv,
        'dashboard_emails': get_dashboard_emails(request)
    })


@login_required
def create_resource(request):
    if request.POST:
        form = ResourceForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                resource = form.save()
                submit = ResourceSubmission(user=request.user,
                                            resource=resource,
                                            type='c')
                submit.save()
            return redirect(settings.MOUNTED_AT + '/resources')
    else:
        if request.GET and 'objective' in request.GET:
            initial = {'objective': request.GET['objective']}
        else:
            initial = {}
        form = ResourceForm(initial=initial)

    args = {'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'resources/create_resource.html', args)


@login_required
def comment_on_resource(request, resource_id):
    if request.POST:
        form = ResourceSubmissionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    # The user could have changed the resource in the form.
                    # Pick up the selected value.
                    resource_id = form.cleaned_data['resource'].id
                    obj.user = request.user
                    obj.save()
                    resource = Resource.objects.get(id=resource_id)
                    if obj.type == 'v':
                        resource.votes = F('votes') + 1
                    else:
                        assert obj.type == 'f'
                        resource.inappropriate_flags = F('inappropriate_flags') + 1
                    resource.save()
                return redirect(settings.MOUNTED_AT + '/resources')
            except IntegrityError:
                # User will have to guess what the problem is.
                pass
    else:
        initial = {'resource': resource_id}
        form = ResourceSubmissionForm(initial=initial)

    args = {'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))

    args['form'] = form
    args['resource_id'] = resource_id
    return render(request, 'resources/comment.html', args)
