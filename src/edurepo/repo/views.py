from django.shortcuts import render
from django.http import HttpResponse
from repo.models import Course


def index(request):
    course_list = Course.objects.order_by('id')
    output = ', '.join([c.description for c in course_list])
    return HttpResponse(output)


def detail(request, class_id):
    return HttpResponse("class %s" % class_id)
