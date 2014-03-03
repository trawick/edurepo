from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from repo.models import Course, ICan, LearningObjective, MultipleChoiceItem, GlossaryItem, ReferenceText, TrueFalseItem


def index(request):
    course_list = Course.objects.order_by('id')
    context = RequestContext(request, {'course_list': course_list})
    return render(request, 'repo/index.html', context)


def detail(request, course_id):
    course = Course.objects.get(id=course_id)
    objective_list = LearningObjective.objects.filter(course=course_id)
    context = RequestContext(request, {'objective_list': objective_list,
                                       'course': course,
                                       'course_id': course_id})
    return render(request, 'repo/course.html', context)


def by_objective(request, course_id, objective_id):
    objective = LearningObjective.objects.get(id=objective_id)
    ican_items = ICan.objects.filter(learning_objective=objective_id)
    glossary_items = GlossaryItem.objects.filter(learning_objective=objective_id)
    multiple_choice_items = MultipleChoiceItem.objects.filter(learning_objective=objective_id)
    tf_items = TrueFalseItem.objects.filter(learning_objective=objective_id)
    reference_text = ReferenceText.objects.filter(learning_objective=objective_id)
    if reference_text:
        reference_text = reference_text[0]
    context = RequestContext(request, {'course_id': course_id,
                                       'objective': objective,
                                       'objective_id': objective_id,
                                       'reference_text': reference_text,
                                       'glossary_items': glossary_items,
                                       'ican_items': ican_items,
                                       'multiple_choice_items': multiple_choice_items,
                                       'tf_items': tf_items})
    return render(request, 'repo/objective.html', context)


def logout(request):
    auth_logout(request)
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    # XXX This is probably wrong (this app mounted on "/"???)
    return redirect('/')
