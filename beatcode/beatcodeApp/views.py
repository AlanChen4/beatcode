from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json

from .models import ProblemSet, ProblemToProblemSet, Submission, Category, Problem

class Home(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'foo': 'bar'})

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

class CategoryView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        category_dict = {}

        # query = """SELECT P.category, MAX(S.sub_date) AS most_recent_sub
        #             FROM beatcodeApp_submission S JOIN beatcodeApp_problem P ON S.problem_id = P.id
        #             GROUP BY P.category
        #             ORDER BY ASC most_recent_sub"""

        query = "SELECT * FROM beatcodeApp_problem"

        for cat in Submission.objects.raw(query):
            category_dict[cat.id] = cat.name
            print(cat.name)

        # for f in Submission._meta.fields: print(f)
        # beatcodeApp.Submission.id
        # beatcodeApp.Submission.user
        # beatcodeApp.Submission.problem
        # beatcodeApp.Submission.sub_date
        # beatcodeApp.Submission.runtime
        # beatcodeApp.Submission.mem_used
        # beatcodeApp.Submission.success

        context['category'] = category_dict

        return render(request, 'beatcodeApp/category.html', context)
