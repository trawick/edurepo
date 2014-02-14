from django.shortcuts import render
from django.template import RequestContext
from repo.models import Course, LearningObjective, GlossaryItem, TrueFalseItem


def index(request):
    course_list = Course.objects.order_by('id')
    context = RequestContext(request, {'course_list': course_list})
    return render(request, 'repo/index.html', context)


def detail(request, course_id):
    objective_list = LearningObjective.objects.filter(course=course_id)
    context = RequestContext(request, {'objective_list': objective_list,
                                       'course_id': course_id})
    return render(request, 'repo/course.html', context)


def by_objective(request, course_id, objective_id):
    glossary_items = GlossaryItem.objects.filter(learning_objective=objective_id)
    tf_items = TrueFalseItem.objects.filter(learning_objective=objective_id)
    context = RequestContext(request, {'glossary_items': glossary_items,
                                       'tf_items': tf_items})
    return render(request, 'repo/objective.html', context)
