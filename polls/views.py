from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Question


# Create your views here.
def index(request: HttpRequest):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
    # same as
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))


def result(request: HttpRequest, question_id: int):
    return HttpResponse(f'Looking for result question {question_id}')


def detail(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request: HttpRequest, question_id: int):
    return HttpResponse(f"Vote for question {question_id}")

