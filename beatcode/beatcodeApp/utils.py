import uuid
import time
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from authentication.models import CustomUser
from .models import Category, Problem, Submission
from scraper import get_problem_info

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        

    def formatday(self, day, submissions):        
        isValidDate = True
        try:
            datetime(self.year, self.month, day)
        except ValueError:
            isValidDate = False
        
        if isValidDate:
            currentDate= datetime(self.year, self.month, day).date()
            dayHasSub=len(submissions.filter(sub_date=currentDate))!=0
            today = {True: 'today', False: ' '} [datetime.today().date()==currentDate]
            
            if dayHasSub:
               return f"<td class={today}><span class='date'>{day}</span><img src='static/beatcodeApp/images/beet.png' alt='logo' width='50' height='50'></td>"
            return f"<td class={today}><span class='date'>{day}</span></td>"
 
        return '<td></td>'
        

    def formatweek(self, theweek, submissions):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, submissions)
        return f'<tr style=" textAlign:center "> {week} </tr>'

    def get_as_html(self):
        submissions = Submission.objects.filter(sub_date__year=self.year, sub_date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=True)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, submissions)}\n'
        return cal


def populate_dummy_data(number_of_accounts=100, number_of_submissions=100):
    """
    Populates the database with arbitrary number of accounts/submissions. Used to test scalability.
    """
    # generate accounts, use uuid4 for the username to avoid collisions
    accounts = []
    for _ in range(number_of_accounts):
        account = CustomUser(
            email=f'{uuid.uuid4()}@dummyemail.com',
            first_name='fake_fname',
            last_name='fake_lname',
            password='password',
            leetcode_username=f'fakeleetcodeusername-{uuid.uuid4()}',
        )
        accounts.append(account)
    CustomUser.objects.bulk_create(accounts)

    # generate submissions for each newly generate accounts
    submissions = []
    if len(Problem.objects.all()) <= 0:
        raise Exception('Could not generate submissions since there are no valid problems in the database')
    random_problem = Problem.objects.all()[0]
    for account in accounts:
        for _ in range(number_of_submissions):
            submission = Submission(
                user=account,
                problem=random_problem,
                sub_date=datetime.now(),
                runtime=0,
                mem_used=0,
                success=False
            )
            submissions.append(submission)
    Submission.objects.bulk_create(submissions)
    

def update_problems():
    """
    For every problem, update/populate all of their information if not already in there (difficulty, categories, etc.)
    """
    problems = Problem.objects.all()

    for problem in problems:
        while True:
            problem_info = get_problem_info(problem.name)
            if problem_info == -1:
                continue
            # create new categories if found category that doesn't already exist
            for category in problem_info['categories']:
                if not Category.objects.filter(name=category).exists():
                    Category.objects.create(name=category)
            
            # get the categories that the problem belongs to
            for category in problem_info['categories']:
                problem.category.add(Category.objects.get(name=category))
            problem.difficulty=problem_info['difficulty']
            problem.save()
            print(f"Updated {problem.name}")
            time.sleep(1)
            break