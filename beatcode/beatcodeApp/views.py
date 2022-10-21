from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import ProblemSet, ProblemToProblemSet


class Home(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'foo': 'bar'})


class ProblemSetView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        problem_set_name = kwargs['problem_set_name']
        problem_set = ProblemSet.objects.get(name=problem_set_name)
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