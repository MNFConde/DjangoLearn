from .models import Question
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import (
    render,
    get_object_or_404,    
)

def index(request):
    lastest_questions = Question.objects.order_by("-pub_date")[:5]
    # print(lastest_questions)
    index_template = loader.get_template('polls/index.html')
    return HttpResponse(index_template.render(
        {'latest_question_list': lastest_questions},
        request,
    ))

def index_second(request):
    lastest_question = Question.objects.order_by("-pub_date")[:5]
    return render(
        request,
        "polls/index.html",
        {
            'latest_question_list': lastest_question,
        },
    )

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request,
        'polls/detail.html',
        {
            'question': question,
        },
    )

def results(request, question_id):
    return HttpResponse(f"正在查看问题结果 {question_id}")
    
def vote(request, question_id):
    return HttpResponse(f"给问题 {question_id} 投票")

