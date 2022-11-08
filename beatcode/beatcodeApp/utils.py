from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Submission

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
            today= {True:'today', False:''} [datetime.today().date()==currentDate]
            
            if datetime.today().date()==currentDate:
                return f"<td class= {today} ><span class='date'>{day}</span></td>"
            
            if dayHasSub:
               return f"<td class={today}><span class='date'>{day}</span><img src='static/beatcodeApp/images/beet.png' alt='logo' width='50' height='50'></td>"
            return f"<td class={today}><span class='date'>{day}</span></td>"
 
        return '<td></td>'
        

    def formatweek(self, theweek, submissions):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, submissions)
        return f'<tr style=" textAlign:center "> {week} </tr>'

    # formats a month as a table
    def formatmonth(self):
        submissions = Submission.objects.filter(sub_date__year=self.year, sub_date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=True)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, submissions)}\n'
        return cal