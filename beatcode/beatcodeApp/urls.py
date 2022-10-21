from django.urls import path
from .views import *


urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('problem-set/<uuid:problem_set_id>/', ProblemSetView.as_view(), name='problem-set'),
    path('chart/', Chart.as_view(), name='chart'),
    path('category-suggestions', CategoryView.as_view(), name="category-suggestions"),
]