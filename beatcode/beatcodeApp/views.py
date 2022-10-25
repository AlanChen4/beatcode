from django.shortcuts import render
from django.views import View
import json

from .models import ProblemSet, ProblemToProblemSet, Submission, User, Category, ToDo

from authentication.models import CustomUser

class Home(View):

    def get(self, request, *args, **kwargs):
        context = {}
        leetcode_username = request.GET.get('username', None)
        if CustomUser.objects.filter(leetcode_username=leetcode_username).exists():
            user = CustomUser.objects.get(leetcode_username=leetcode_username)
            submissions = Submission.objects.filter(user=user)
            problems = [submission.problem for submission in submissions]
            context['problems'] = problems
        else:
            context['problems'] = []
        return render(request, 'beatcodeApp/home.html', context)

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
    
    
class UserSubmissionView(View):
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
            print(filtered_subs)
            
        context['user'] = user
        context['submissions'] = filtered_subs
                
        return render(request, 'beatcodeApp/user-submissions.html', context)
                


class Todo(View):
    #get all to do items from a specific user

    def get(self,request, *args, **kwargs):
        context = {}

        #using ORM filter since it would be redundant to query by user as all the problems are created by a super user
        # will potentially replace with raw SQL query. 
        todo_problems = ToDo.objects.filter(user=request.user)
       
        #print(todo_problems)
        #context['ToDo List'] = todolist # not really sure how to obtain list like numbering? 
        #i'm thinking to display like a table like this:
        #  Todo # | Problem
        #   1     | DP problem 1
        #   2     | Binary Tree problem 3 
        # ... 
        
        #problems are displayed in the orde that they are added. 
        context['problems'] = todo_problems
        return render(request, 'beatcodeApp/todos.html',context)

class CategoryView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        category_to_activity = {}

        query = """SELECT C.category, C.id, MAX(sub_date) AS recent_activity
                    FROM beatcodeApp_category C LEFT OUTER JOIN
                    (beatcodeApp_problem P LEFT OUTER JOIN beatcodeApp_submission S ON P.id = S.problem_id)
                    ON C.id = P.category_id
                    GROUP BY P.category_id
                    ORDER BY recent_activity ASC"""

        for cat in Submission.objects.raw(query):
            category_to_activity[cat.category] = cat.recent_activity

        context['category_to_activity'] = category_to_activity

        return render(request, 'beatcodeApp/category.html', context)
