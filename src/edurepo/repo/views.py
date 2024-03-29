from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

from edurepo import settings
from repo.models import Course, ICan, LearningObjective, MultipleChoiceItem, GlossaryItem, ReferenceText, TrueFalseItem
from teachers.views import get_dashboard_emails


def index(request):
    course_list = Course.objects.order_by('cat__id', 'id')
    return render(request, 'repo/index.html', {
        'course_list': course_list,
        'dashboard_emails': get_dashboard_emails(request)
    })


def detail(request, course_id):
    course = Course.objects.get(id=course_id)
    objective_list = LearningObjective.objects.filter(course=course_id).order_by('id')
    return render(request, 'repo/course.html', {
        'objective_list': objective_list,
        'course': course,
        'course_id': course_id,
        'dashboard_emails': get_dashboard_emails(request)
    })


def by_objective(request, course_id, objective_id):
    objective = LearningObjective.objects.get(id=objective_id)
    ican_items = ICan.objects.filter(learning_objective=objective_id)
    glossary_items = GlossaryItem.objects.filter(learning_objective=objective_id)
    multiple_choice_items = MultipleChoiceItem.objects.filter(learning_objective=objective_id)
    tf_items = TrueFalseItem.objects.filter(learning_objective=objective_id)
    try:
        reference_text = objective.referencetext
    except ObjectDoesNotExist:
        reference_text = None
    return render(request, 'repo/objective.html', {
        'course_id': course_id,
        'objective': objective,
        'objective_id': objective_id,
        'reference_text': reference_text,
        'glossary_items': glossary_items,
        'ican_items': ican_items,
        'multiple_choice_items': multiple_choice_items,
        'tf_items': tf_items,
        'dashboard_emails': get_dashboard_emails(request)
    })


def logout(request):
    auth_logout(request)
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return redirect(settings.MOUNTED_AT + '/')
