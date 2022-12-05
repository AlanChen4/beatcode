from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.utils.safestring import mark_safe
from .utils import Calendar
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import (
    CreateView,
    UpdateView,
)
import json

from .models import *
from authentication.models import CustomUser

class Home(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        # context variables for the "Problems Completed" component
        # use submissions by user to collect problems and categories completed
        submissions = Submission.objects.filter(user=request.user, success=True)
        category_count = {}
        for submission in submissions:
            # categories belonging to submission's problem
            categories = submission.problem.category.all()

            # count each category that the problem belongs to
            for category in categories:
                category_count[category.name] = category_count.get(category.name, 0) + 1
                
        context['categories'] = json.dumps(list(category_count.keys()))
        context['problem_freq'] = json.dumps(list(category_count.values()))    

        # context variables for the "Least Practiced" component
        # use submissions with their associated submission date to determine the least practiced categories
        category_dates = {c.name:'0' for c in Category.objects.all()}
        for submission in submissions.order_by('sub_date'):
            for category in submission.problem.category.all():
                category_dates[category.name] = str(submission.sub_date)
        category_dates_sorted = sorted(category_dates.items(), key=lambda item: item[1])
        # select the bottom 3 results - these are the least practiced
        least_practiced = category_dates_sorted[:3]
        # replace '0' with 'N/A' since this means that the category has never been practiced
        for i in range(len(least_practiced)):
            if least_practiced[i][1] == '0':
                # having to construct new tuple since tuples are immutable
                least_practiced[i] = (least_practiced[i][0], 'N/A')
        context['least_practiced'] = least_practiced

        # context variables for the "Streaks" component
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth() #returns cal as a table w new methods in utils.py
        context['calendar'] = mark_safe(html_cal)     
        
        streak = 0
        currDate=d.date()
        while(True):
            if len(Submission.objects.filter(sub_date=currDate))!=0:
                streak+=1
                currDate=currDate-timedelta(days=1)
            else:
                break

        context['streak']= str(streak) + {True: " day", False: " days"} [streak==1]
        
        # context variables for the "TODO" component
        todo_problems = ToDo.objects.filter(user=request.user, complete=False)
        context['todo_problems'] = todo_problems
        
        return render(request, 'beatcodeApp/home.html', context)

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

class ProblemSetView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        # get the problem set corresponding to the kwarg argument
        problem_set_id = kwargs['problem_set_id']
        problem_set = ProblemSet.objects.get(id=problem_set_id)

        # only add problems that are a part of the specified problem set
        problems = []
        for problem in Problem.objects.all().order_by('name'):
            if problem_set in problem.problem_set.all():
                problems.append(problem)

        # filter problems based on searched category
        searched_category = request.GET.get('category', None)
        if searched_category != None and searched_category != '':
            problems = list(filter(lambda x: searched_category.lower() in set(c.name.lower() for c in x.category.all()), problems))

        context['problems'] = problems

        return render(request, 'beatcodeApp/problemSet.html', context)

class ProblemView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        problem_id = kwargs['problem_id']
        problem = Problem.objects.get(id=problem_id)

        context['problem'] = problem
        return render(request, 'beatcodeApp/problem.html', context)

    def post(self, request, *args, **kwargs):
        context = {}

        problem_id = kwargs['problem_id']
        problem = Problem.objects.get(id=problem_id)
        ToDo.objects.create(user=request.user,problem=problem)
        
        context['problem'] = problem
        return render(request, 'beatcodeApp/problem.html', context)

class ProblemSetListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}
        problem_sets = ProblemSet.objects.all()
        context['problem_sets'] = problem_sets
        return render(request, 'beatcodeApp/problemSetList.html', context)

class Chart(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        submissions = Submission.objects.filter(user=request.user, success=True)
        categories = {}
        for submission in submissions:
            categories[submission.problem.category.category] = categories.get(submission.problem.category, 0) + 1
        context['categories'] = json.dumps(list(categories.keys()))
        context['problem_freq'] = json.dumps(list(categories.values()))
        return render(request, 'beatcodeApp/chart.html', context)
    
class UserSubmissionView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}
        
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)
        all_subs = Submission.objects.filter(user_id=user_id)
        
        query= '''SELECT S.id, P.category_id, C.category 
                    FROM beatcodeApp_submission S, beatcodeApp_problem P, beatcodeApp_category C 
                    WHERE S.problem_id = P.id AND C.id=P.category_id AND S.success=1
                    ORDER BY sub_date DESC'''
             
        submissions = all_subs.raw(query)
        
        desired_category = request.GET.get('category')
        
        filtered_subs = []
        if desired_category == None or desired_category =='':
            filtered_subs = all_subs
        else:
            for sub in submissions:
                if desired_category.lower() == sub.category.lower():
                    filtered_subs.append(sub)
                    if len(filtered_subs)==5:
                        break
            
        context['user'] = user
        context['submissions'] = filtered_subs
                
        return render(request, 'beatcodeApp/user-submissions.html', context)

class Todo(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}

        # using ORM filter since it would be redundant to query by user as all the problems are created by a super user
        todo_problems = ToDo.objects.filter(user=request.user)
        
        # problems are displayed in the order that they are added
        context['problems'] = todo_problems
        return render(request, 'beatcodeApp/todos.html',context)

class CategoryView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}
        
        # use submissions with their associated submission date to determine the least practiced categories
        submissions = Submission.objects.filter(user=request.user, success=True)
        category_dates = {c.name:'0' for c in Category.objects.all()}
        for submission in submissions.order_by('sub_date'):
            for category in submission.problem.category.all():
                category_dates[category.name] = str(submission.sub_date)
        category_dates_sorted = sorted(category_dates.items(), key=lambda item: item[1])
        # select the bottom 3 results - these are the least practiced
        least_practiced = category_dates_sorted[:3]
        # replace '0' with 'N/A' since this means that the category has never been practiced
        for i in range(len(least_practiced)):
            if least_practiced[i][1] == '0':
                # having to construct new tuple since tuples are immutable
                least_practiced[i] = (least_practiced[i][0], 'N/A')
        
        context['least_practiced'] = least_practiced

        return render(request, 'beatcodeApp/category.html', context)
