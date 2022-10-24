from django.shortcuts import render
from django.views import View
import json

from .models import ProblemSet, ProblemToProblemSet, Submission, ToDo


class Home(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'beatcodeApp/home.html')


class ProblemSetView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        problem_set_id = kwargs['problem_set_id']
        problem_set = ProblemSet.objects.get(id=problem_set_id)
        problems = [ps.problem for ps in ProblemToProblemSet.objects.filter(problem_set=problem_set)]

        desired_category = request.GET.get('category')
        filtered_problems = []
        if desired_category == None or desired_category=='': 
            filtered_problems = problems
        else:  
            for problem in problems:
                categories = [c.get_category_display().lower() for c in set(problem.category.all())]
                if desired_category.lower() in categories: 
                    filtered_problems.append(problem)
            print(filtered_problems)
        context['problem_set'] = problem_set
        context['problems'] = filtered_problems
        return render(request, 'beatcodeApp/problemSet.html', context)

class Chart(View):
    #get all successful problems and their category
    def get(self, request, *args, **kwargs):
        context = {}

        submissions = Submission.objects.filter(user=request.user, success=True)
        categories = {}
        for submission in submissions:
            categories[submission.problem.category.category] = categories.get(submission.problem.category, 0) + 1

        print(categories)
        context['categories'] = json.dumps(list(categories.keys()))
        context['problem_freq'] = json.dumps(list(categories.values()))
        return render(request, 'beatcodeApp/chart.html', context)


class Todo(View):
    #get all to do items from a specific user

    def get(self,request, *args, **kwargs):
        context = {}

        todo_problems = ToDo.objects.filter(user=request.user, success=True)
        #context['ToDo List'] = todolist # not really sure how to obtain list like numbering? 
        #i'm thinking to display like a table like this:
        #  Todo # | Problem
        #   1     | DP problem 1
        #   2     | Binary Tree problem 3 
        # ... 
        context['problems'] = todo_problems
        return render(request, 'beatcodeApp/todos.html',context)