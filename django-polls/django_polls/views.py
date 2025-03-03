from django.db.models.query import QuerySet
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self) -> QuerySet[Question]:
        """Return the last five published questions"""
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(
                has_choices=Exists(Choice.objects.filter(question=OuterRef("pk")))
            )
            .filter(has_choices=True)
            .order_by("-pub_date")[:5]
        )


class DetailsView(generic.DetailView):
    template_name = "polls/details.html"
    model = Question

    def get_queryset(self):
        """exclude any questions that are not published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now()).annotate(
            has_choices=Exists(Choice.objects.filter(question=OuterRef("pk")))
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """exclude any questions that are not published yet"""
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(
                has_choices=Exists(Choice.objects.filter(question=OuterRef("pk")))
            )
            .filter(has_choices=True)
        )


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])  # type: ignore
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/details.html",
            {"question": question, "error_message": "you did not select a choice"},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
