from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.shortcuts import render, get_object_or_404, reverse

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


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
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/result.html', {'question': question})

def detail(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You don't choose choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

