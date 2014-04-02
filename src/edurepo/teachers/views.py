from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import RequestContext
from edurepo import settings
from teachers.models import Teacher, TeacherClass, Entry
from teachers.forms import TeacherForm, TeacherClassForm


def get_dashboard_emails(request):
    """does request.user refer to a teacher with a dashboard?
    return link if so"""
    if not request.user or not request.user.is_authenticated():
        return None
    user = User.objects.get(username=request.user)
    try:
        teachers = Teacher.objects.filter(user=user)
    except Teacher.DoesNotExist:
        return None
    return [teacher.email for teacher in teachers]


def index(request):
    teacher_list = Teacher.objects.order_by('email')
    context = RequestContext(request, {'teacher_list': teacher_list,
                                       'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'teachers/index.html', context)


def detail(request, teacher_email):
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    teacher = Teacher.objects.get(email=teacher_email)
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'teacher': teacher,
                                       'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'teachers/classes.html', context)


def events(request, teacher_email, class_name):
    teacher = Teacher.objects.get(email=teacher_email)
    entry_list = Entry.objects.filter(teacher=teacher_email, teacher_class__name=class_name)
    context = RequestContext(request, {'entry_list': entry_list,
                                       'teacher': teacher,
                                       'class_name': class_name,
                                       'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'teachers/entries.html', context)


@login_required
def register_teacher(request):
    if request.POST:
        form = TeacherForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('../..')
    else:
        initial = {}
        form = TeacherForm(initial=initial)

    args = {}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/register_teacher.html', args)


def request_to_provider(request):
    root = settings.MOUNTED_AT + '/'
    return request.build_absolute_uri(root)


@login_required
def add_class(request, teacher_email):
    if request.POST:
        form = TeacherClassForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            teacher = Teacher.objects.get(email=teacher_email)
            obj.teacher = teacher
            obj.save()
            return redirect('../..')
    else:
        initial = {'repo_provider': request_to_provider(request)}
        form = TeacherClassForm(initial=initial)

    args = {'teacher_email': teacher_email}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/add_class.html', args)


@login_required
def dashboard(request, teacher_email):
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    teacher = Teacher.objects.get(email=teacher_email)
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'teacher': teacher,
                                       'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'teachers/dashboard.html', context)
