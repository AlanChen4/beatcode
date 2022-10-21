from django.urls import path
from .views import *


urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('problem-set/<str:problem_set_name>/', ProblemSetView.as_view(), name='problem-set'),
    path('chart/', Chart.as_view(), name='chart'),
]