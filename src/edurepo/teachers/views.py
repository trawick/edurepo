import datetime
from django.db import IntegrityError, transaction
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
    """
    register_teacher() always creates the registration using the logged-in
    User, so no additional security checks are required.
    :param request:
    :return:
    """
    if request.POST:
        form = TeacherForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
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
    """
    add_class() creates the TeacherClass using the teacher_email in the URL,
    so we must also validate that against the logged-in User.
    :param request:
    :param teacher_email:
    :return:
    """
    teacher = Teacher.objects.get(email=teacher_email)
    if teacher.user != request.user:
        # weird mistake or evil to manipulate another person's data?  start over
        return redirect('top.index')

    if request.POST:
        form = TeacherClassForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.teacher = teacher
                    obj.save()
                return redirect('../..')
            except IntegrityError:
                # bad bad bad; I guess the TeacherClassForm has to be initialized
                # with the teacher so that its clean() method can look at it.
                form._errors['name'] = ['You already created a class of this name.']
    else:
        initial = {'repo_provider': request_to_provider(request)}
        form = TeacherClassForm(initial=initial)

    args = {'teacher_email': teacher_email,
            'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/add_class.html', args)


@login_required
def edit_class(request, teacher_email, teacher_class_id):
    teacher = Teacher.objects.get(email=teacher_email)

    if teacher.user != request.user:
        # weird mistake or evil to manipulate another person's data?  start over
        return redirect('top.index')

    teacher_class = TeacherClass.objects.get(id=teacher_class_id)
    if request.POST:
        if 'delete-button' in request.POST:
            teacher_class.delete()
            return redirect('teachers.views.dashboard', teacher_email=teacher_email)
        else:
            form = TeacherClassForm(request.POST, instance=teacher_class)
            if form.is_valid():
                form.save()
                return redirect('teachers.views.dashboard', teacher_email=teacher_email,
                                teacher_class_id=teacher_class_id)
    else:
        initial = {'name': teacher_class.name,
                   'course_id': teacher_class.course_id,
                   'repo_provider': request_to_provider(request),
                   }
        form = TeacherClassForm(initial=initial)

    args = {'teacher_email': teacher_email,
            'dashboard_emails': get_dashboard_emails(request),
            'teacher_class_id': teacher_class_id
            }
    args.update(csrf(request))

    args['form'] = form
    return render(request, 'teachers/edit_class.html', args)


@login_required
def add_objective(request, teacher_email, teacher_class_id, date):
    """
    add_objective() creates the Entry using the teacher_email and
    teacher_class_id in the URL, so we must also validate that
    against the logged-in User.
    :param request:
    :param teacher_email:
    :param teacher_class_id:
    :param date:
    :return:
    """
    teacher = Teacher.objects.get(email=teacher_email)
    if teacher.user != request.user:
        # weird mistake or evil to manipulate another person's data?  start over
        return redirect('top.index')

    teacher_class = TeacherClass.objects.get(id=teacher_class_id)

    if request.POST:
        form = EntryForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    entry = form.save(commit=False)
                    entry.teacher = teacher
                    entry.teacher_class = teacher_class
                    entry.date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    entry.save()
                start_of_week_datetime = entry.date - datetime.timedelta(days=entry.date.weekday())
                start_of_week = datetime.date(start_of_week_datetime.year, start_of_week_datetime.month,
                                              start_of_week_datetime.day)
                return redirect('teachers.views.dashboard', teacher_email=teacher_email,
                                teacher_class_id=teacher_class_id, start_of_week=start_of_week)
            except IntegrityError:
                # bad bad bad; I guess the EntryForm has to be initialized
                # with the date and teacher so that its clean() method can look at it.
                form._errors['objective'] = ['This objective is already on the calendar for this day.']
                pass
    else:
        objectives = objectives_for_course(teacher_class.course_id, teacher_class.repo_provider)
        if not objectives:
            # XXX fail with an error message
            pass
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
    """
    remove_objective() deletes the Entry using the teacher_email and
    teacher_class_id in the URL, so we must also validate that
    against the logged-in User.

    :param request:
    :param teacher_email:
    :param teacher_class_id:
    :param date:
    :param objective:
    :return:
    """
    teacher = Teacher.objects.get(email=teacher_email)

    if teacher.user != request.user:
        # weird mistake or evil to manipulate another person's data?  start over
        return redirect('top.index')

    if request.POST:
        date_of_objective = datetime.datetime.strptime(date, '%Y-%m-%d')
        Entry.objects.filter(teacher=teacher, teacher_class__id=teacher_class_id,
                             date=date_of_objective, objective=objective).delete()
        start_of_week_datetime = date_of_objective - datetime.timedelta(days=date_of_objective.weekday())
        start_of_week = datetime.date(start_of_week_datetime.year, start_of_week_datetime.month,
                                      start_of_week_datetime.day)
        return redirect('teachers.views.dashboard', teacher_email=teacher_email, teacher_class_id=teacher_class_id,
                        start_of_week=start_of_week)

    args = {'teacher_email': teacher_email,
            'teacher_class_id': teacher_class_id,
            'date': date,
            'objective': objective,
            'dashboard_emails': get_dashboard_emails(request)}
    args.update(csrf(request))
    return render(request, 'teachers/remove_objective.html', args)


@login_required
def dashboard(request, teacher_email, teacher_class_id=None, start_of_week=None):
    """
    dashboard() creates the dashboard based on fields in the URL, so we must
    also validate that based on the logged in User.
    :param request:
    :param teacher_email:
    :param teacher_class_id:
    :param start_of_week:
    :return:
    """
    teacher_class_list = TeacherClass.objects.filter(teacher=teacher_email)
    teacher = Teacher.objects.get(email=teacher_email)

    if teacher.user != request.user:
        # weird mistake or evil to manipulate another person's data?  start over
        return redirect('top.index')

    if teacher_class_list:
        if not teacher_class_id:
            # if the teacher has no classes, we won't redirect here, and the
            # user will get a dashboard with appropriate text
            return redirect('teachers.views.dashboard', teacher_email=teacher_email,
                            teacher_class_id=teacher_class_list[0].id)
        if not start_of_week:
            today = datetime.date.today()
            return redirect('teachers.views.dashboard', teacher_email=teacher_email,
                            teacher_class_id=teacher_class_id,
                            start_of_week=today - datetime.timedelta(days=today.weekday()))

    selected_class = None
    previous_week_link = None
    next_week_link = None
    for c in teacher_class_list:
        c.active_class = ''
        if int(teacher_class_id) == c.id:
            c.active_class = 'active'
            selected_class = c
            c.days = dict()
            c.dates = dict()
            c.objectives = dict()
            cur_day_in_datetime = datetime.datetime.strptime(start_of_week, '%Y-%m-%d')
            cur_day = datetime.date(cur_day_in_datetime.year, cur_day_in_datetime.month, cur_day_in_datetime.day)
            previous_week = cur_day - datetime.timedelta(days=7)
            previous_week_redirect = redirect('teachers.views.dashboard', teacher_email=teacher_email,
                                              teacher_class_id=teacher_class_id,
                                              start_of_week=previous_week)
            previous_week_link = previous_week_redirect.url
            next_week = cur_day + datetime.timedelta(days=7)
            next_week_redirect = redirect('teachers.views.dashboard', teacher_email=teacher_email,
                                          teacher_class_id=teacher_class_id,
                                          start_of_week=next_week)
            next_week_link = next_week_redirect.url
            for day in day_letters:
                c.dates[day] = cur_day.strftime('%Y-%m-%d')
                entries_for_day = Entry.objects.filter(teacher=teacher, teacher_class=c).filter(date=cur_day)
                objectives_and_descriptions = []
                for entry in entries_for_day:
                    description = description_for_objective(entry.objective, c.repo_provider)
                    objectives_and_descriptions += [(entry.objective, description)]
                c.objectives[day] = objectives_and_descriptions
                cur_day += datetime.timedelta(days=1)
    if teacher_class_list:
        assert selected_class
    context = RequestContext(request, {'teacher_class_list': teacher_class_list,
                                       'selected_class': selected_class,
                                       'day_names': day_names,
                                       'day_letters': ['M', 'T', 'W', 'R', 'F'],
                                       'teacher': teacher,
                                       'dashboard_emails': get_dashboard_emails(request),
                                       'start_of_week': start_of_week,
                                       'previous_week_link': previous_week_link,
                                       'next_week_link': next_week_link})
    return render(request, 'teachers/dashboard.html', context)
