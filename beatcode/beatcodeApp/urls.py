from django.urls import path
from .views import *


urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('problem-set/<uuid:problem_set_id>/', ProblemSetView.as_view(), name='problem-set'),
]