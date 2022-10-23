from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json

from .models import ProblemSet, ProblemToProblemSet, Submission

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
        category_to_activity = {}

        query = """SELECT C.category, C.id, MAX(sub_date) AS recent_activity
                    FROM beatcodeApp_submission S JOIN beatcodeApp_problem P ON S.problem_id = P.id
                    JOIN beatcodeApp_category C ON P.category_id = C.id
                    GROUP BY P.category_id
                    ORDER BY recent_activity ASC"""

        for cat in Submission.objects.raw(query):
            category_to_activity[cat.category] = cat.recent_activity

        context['category_to_activity'] = category_to_activity

        return render(request, 'beatcodeApp/category.html', context)
