from django.shortcuts import render
from teachers.views import get_dashboard_emails


def welcome(request):
    return render(request, 'index.html', {
        'dashboard_emails': get_dashboard_emails(request)
    })
