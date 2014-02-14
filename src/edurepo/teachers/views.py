from django.shortcuts import render
from django.template import RequestContext
from teachers.models import Teacher, Course, Entry


def index(request):
    teacher_list = Teacher.objects.order_by('email')
    context = RequestContext(request, {'teacher_list': teacher_list})
    return render(request, 'teachers/index.html', context)


def detail(request, teacher_id):
    course_list = Course.objects.filter(teacher=teacher_id)
    context = RequestContext(request, {'course_list': course_list,
                                       'teacher_id': teacher_id})
    return render(request, 'teachers/courses.html', context)


def events(request, teacher_id, course_id):
    entry_list = Entry.objects.filter(teacher=teacher_id, course__name=course_id)
    context = RequestContext(request, {'entry_list': entry_list,
                                       'teacher_id': teacher_id,
                                       'course_id': course_id})
    return render(request, 'teachers/entries.html', context)
