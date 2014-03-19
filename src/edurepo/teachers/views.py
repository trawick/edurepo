from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from teachers.models import Teacher, TeacherClass, Entry
from teachers.forms import TeacherForm, TeacherClassForm


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


@login_required
def register_teacher(request):
    if request.POST:
        form = TeacherForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/teachers')
    else:
        initial = {}
        form = TeacherForm(initial=initial)

    args = {}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/register_teacher.html', args)


@login_required
def add_class(request, teacher_email):
    if request.POST:
        form = TeacherClassForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            teacher = Teacher.objects.get(email=teacher_email)
            obj.teacher = teacher
            obj.save()
            return redirect('/teachers')
    else:
        initial = {}
        form = TeacherClassForm(initial=initial)

    args = {'teacher_email': teacher_email}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/add_class.html', args)
