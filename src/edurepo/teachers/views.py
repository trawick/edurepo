from django.shortcuts import render
from django.template import RequestContext
from teachers.models import Teacher, TeacherClass, Entry


def index(request):
    teacher_list = Teacher.objects.order_by('email')
    context = RequestContext(request, {'teacher_list': teacher_list})
    return render(request, 'teachers/index.html', context)


def detail(request, teacher_email):
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    teacher = Teacher.objects.get(email=teacher_email)
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'teacher': teacher})
    return render(request, 'teachers/classes.html', context)


def events(request, teacher_email, class_name):
    teacher = Teacher.objects.get(email=teacher_email)
    entry_list = Entry.objects.filter(teacher=teacher_email, teacher_class__name=class_name)
    context = RequestContext(request, {'entry_list': entry_list,
                                       'teacher': teacher,
                                       'class_name': class_name})
    return render(request, 'teachers/entries.html', context)
