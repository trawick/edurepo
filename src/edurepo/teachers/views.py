import datetime
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import RequestContext
from edurepo import settings
from teachers.models import Teacher, TeacherClass, Entry
from teachers.forms import EntryForm, TeacherForm, TeacherClassForm, create_entry_form
from core.utils import description_for_objective, objectives_for_course


day_names = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday'}
day_letters = ['M', 'T', 'W', 'R', 'F']


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
    teacher_list = Teacher.objects.order_by('name')
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
    teacher_class = TeacherClass.objects.get(name=class_name)
    entry_list = Entry.objects.filter(teacher=teacher_email, teacher_class__name=class_name).order_by('date')

    # remote lookup of objective description
    for e in entry_list:
        e.description = description_for_objective(e.objective, teacher_class.repo_provider)

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

    args = {'dashboard_emails': get_dashboard_emails(request)}
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

    args = {'teacher_email': teacher_email,
            'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/add_class.html', args)


@login_required
def add_objective(request, teacher_email, teacher_class_id, date):
    teacher_class = TeacherClass.objects.get(id=teacher_class_id)

    if request.POST:
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            teacher = Teacher.objects.get(email=teacher_email)
            entry.teacher = teacher
            entry.teacher_class = teacher_class
            entry.date = datetime.datetime.strptime(date, '%B %d, %Y')
            entry.save()
            return redirect('teachers.views.dashboard', teacher_email=teacher_email, teacher_class_id=teacher_class_id)
    else:
        objectives = objectives_for_course(teacher_class.course_id, teacher_class.repo_provider)
        # like EntryForm() above, but dynamically created to use a selection
        # of objectives specific to this course
        form = create_entry_form(objectives)

    args = {'teacher_email': teacher_email,
            'teacher_class_id': teacher_class_id,
            'dashboard_emails': get_dashboard_emails(request),
            'date': date}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'teachers/add_objective.html', args)


@login_required
def remove_objective(request, teacher_email, teacher_class_id, date, objective):
    if request.POST:
        teacher = Teacher.objects.get(email=teacher_email)
        Entry.objects.filter(teacher=teacher, teacher_class__id=teacher_class_id,
                             date=datetime.datetime.strptime(date, '%B %d, %Y'), objective=objective).delete()
        return redirect('teachers.views.dashboard', teacher_email=teacher_email, teacher_class_id=teacher_class_id)

    args = {'teacher_email': teacher_email,
            'teacher_class_id': teacher_class_id,
            'date': date,
            'objective': objective,
            'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))
    return render(request, 'teachers/remove_objective.html', args)


@login_required
def dashboard(request, teacher_email, teacher_class_id=None):
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    teacher = Teacher.objects.get(email=teacher_email)
    today = datetime.date.today()
    if not teacher_class_id:
        # if the teacher has no classes, we won't redirect here, and the
        # user will get a dashboard with appropriate text
        if teacher_class_list:
            return redirect('teachers.views.dashboard', teacher_email=teacher_email, teacher_class_id=teacher_class_list[0].id)
    selected_class = None
    for c in teacher_class_list:
        c.active_class = ''
        if int(teacher_class_id) == c.id:
            c.active_class = 'active'
            selected_class = c
            c.days = dict()
            c.dates = dict()
            cur_day = today - datetime.timedelta(days=today.weekday())
            for day in day_letters:
                c.dates[day] = cur_day
                c.days[day] = Entry.objects.filter(teacher=teacher, teacher_class=c).filter(date=cur_day)
                cur_day += datetime.timedelta(days=1)
    if teacher_class_list:
        assert selected_class
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'selected_class': selected_class,
                                       'day_names': day_names,
                                       'teacher': teacher,
                                       'dashboard_emails': get_dashboard_emails(request)})
    return render(request, 'teachers/dashboard.html', context)
