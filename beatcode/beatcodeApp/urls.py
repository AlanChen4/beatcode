from django.urls import path
from .views import *


urlpatterns = [
    path('problem-set/<uuid:problem_set_id>/', ProblemSetView.as_view(), name='problem-set'),
    path('problem-sets',ProblemSetListView.as_view(), name='problem-sets'),
    path('problem/<uuid:problem_id>/', ProblemView.as_view(), name='problem'),
    path('chart/', Chart.as_view(), name='chart'),
    path('user-submissions/<uuid:user_id>/', UserSubmissionView.as_view(), name='submissions'),
    path('todos/', Todo.as_view(), name='todos'),
    path('category-suggestions/', CategoryView.as_view(), name="category-suggestions"),
    path('home/', Home.as_view(), name='home'),
    path('', Home.as_view(), name='home'),
]