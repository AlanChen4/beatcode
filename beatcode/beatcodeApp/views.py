from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.utils.safestring import mark_safe
from .utils import Calendar
from datetime import datetime, timedelta
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
        submissions = Submission.objects.filter(user=request.user, success=True)
        category_count = {}
        for submission in submissions:
            categories = submission.problem.category.all()

            for category in categories:
                category_count[category.name] = category_count.get(category.name, 0) + 1
        context['categories'] = json.dumps(list(category_count.keys()))
        context['problem_freq'] = json.dumps(list(category_count.values()))    

        # context variables for the "Least Practiced" component
        least_practiced = {}
        least_practiced_query = """
            SELECT C.name, C.id, MAX(S.sub_date) AS recent_activity
            FROM beatcodeApp_category C LEFT OUTER JOIN
            ((beatcodeApp_problem P JOIN beatcodeApp_problem_category PC ON P.id = PC.problem_id)
            JOIN beatcodeApp_submission S ON P.id = S.problem_id)
            ON C.id = PC.category_id
            GROUP BY C.id
            ORDER BY recent_activity ASC
            LIMIT 5
        """
        for category in Submission.objects.raw(least_practiced_query):
            least_practiced[category.name] = category.recent_activity
        context['least_practiced'] = least_practiced

        # context variables for the "Streaks" component
        today = datetime.today()
        calendar = Calendar(today.year, today.month)
        html_calendar = calendar.get_as_html()
        context['calendar'] = mark_safe(html_calendar)     

        streak = 0
        current_date = today.date()
        while len(Submission.objects.filter(sub_date=current_date)) != 0:
            streak+=1
            current_date=current_date - timedelta(days=1)
        context['streak']= str(streak) + {True: " day", False: " days"} [streak==1]
        
        # context variables for the "Todo" component
        todo_top5 = """
            SELECT * FROM beatcodeApp_todo LIMIT 5
        """
        todo_problems = ToDo.objects.raw(todo_top5)
        context['todo_problems'] = todo_problems
        
        return render(request, 'beatcodeApp/home.html', context)


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
        
        query = '''SELECT S.id, P.category_id, C.category 
                    FROM beatcodeApp_submission S, beatcodeApp_problem P, beatcodeApp_category C 
                    WHERE S.problem_id = P.id AND C.id = P.category_id AND S.success = 1
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

        query_to_delete_problem = '''SELECT P.id
                    FROM (beatcodeApp_todo T JOIN beatcodeApp_problem P
                    ON T.problem_id = P.id)
                    JOIN beatcodeApp_submission S
                    ON (T.problem_id = S.problem_id AND S.success = 1)'''

        for p in ToDo.objects.raw(query_to_delete_problem):
            ToDo.objects.filter(problem_id = p.id).delete()
        
        query_to_add_name = '''SELECT P.id, P.name
                                FROM beatcodeApp_todo T JOIN beatcodeApp_problem P
                                ON T.problem_id = P.id'''

        # problems are displayed in the order that they are added
        context['todos'] = ToDo.objects.raw(query_to_add_name)
        return render(request, 'beatcodeApp/todos.html', context)
        
    def post(self, request, *args, **kwargs):
        context = {}

        problem_id = request.POST['problem_id']
        problem = Problem.objects.get(id=problem_id)
        #print(problem)
        ToDo.objects.filter(user=request.user,problem=problem).delete()
        
        todo_problems = ToDo.objects.filter(user=request.user)
        context['todos'] = todo_problems
        return render(request, 'beatcodeApp/todos.html', context)


class CategoryView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {}
        least_practiced = {}

        query = """SELECT C.name, C.id, MAX(S.sub_date) AS recent_activity
                    FROM beatcodeApp_category C LEFT OUTER JOIN
                    ((beatcodeApp_problem P JOIN beatcodeApp_problem_category PC ON P.id = PC.problem_id)
                    JOIN beatcodeApp_submission S ON P.id = S.problem_id)
                    ON C.id = PC.category_id
                    GROUP BY C.id
                    ORDER BY recent_activity ASC"""
        
        for cat in Submission.objects.raw(query):
            least_practiced[cat.name] = cat.recent_activity
        
        context['least_practiced'] = least_practiced

        return render(request, 'beatcodeApp/category.html', context)
