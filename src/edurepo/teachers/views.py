from django.shortcuts import render
from django.template import RequestContext
from teachers.models import Teacher, TeacherClass, Entry


def index(request):
    teacher_list = Teacher.objects.order_by('email')
    context = RequestContext(request, {'teacher_list': teacher_list})
    return render(request, 'teachers/index.html', context)


def detail(request, teacher_email):
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'teacher_email': teacher_email})
    return render(request, 'teachers/classes.html', context)


def events(request, teacher_email, class_name):
    entry_list = Entry.objects.filter(teacher=teacher_email, teacher_class__name=class_name)
    context = RequestContext(request, {'entry_list': entry_list,
                                       'teacher_email': teacher_email,
                                       'class_name': class_name})
    return render(request, 'teachers/entries.html', context)
