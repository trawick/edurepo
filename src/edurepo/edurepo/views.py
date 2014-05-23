from django.shortcuts import render
from django.template import RequestContext
from teachers.views import get_dashboard_emails


def welcome(request):
    context = RequestContext(request, {'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'index.html', context)
