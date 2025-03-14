from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:question_id>/vote", views.vote, name="vote"),
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/", views.DetailsView.as_view(), name="details"),
]
