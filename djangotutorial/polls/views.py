from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import (
    render,
    get_object_or_404,    
)
from django.db.models import F
from django.urls import reverse

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
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))