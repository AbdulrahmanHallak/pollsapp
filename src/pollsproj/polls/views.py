from asyncio import QueueShutDown
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse

from .models import Question

# Create your views here.


def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_questions": latest_questions}
    return render(request, "polls/index.html", context)


def details(request, question_id):
    question = get_object_or_404(
        Question.objects.prefetch_related("choice_set"), pk=question_id
    )
    return render(request, "polls/details.html", {"question": question})


def vote(request, question_id):
    return HttpResponse("you are voting on question %s" % question_id)


def results(request, question_id):
    return HttpResponse("you are voting on question %s" % question_id)
