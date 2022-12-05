from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from authentication.models import CustomUser
from .models import ToDo


def send():
    email_list = set()
    for person in CustomUser.objects.all():
        for todo in ToDo.objects.filter(user=person):
            if todo.complete == False:
                email_list.add(person.email)
    subject = "Don't forget to practice leetcode today!"        
    message = f"Hi! \n\nWe noticed you haven't completed a leetcode problem on your Todo list for a while. Make sure to take some time today to practice! \nBest, \nBeatcode"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = email_list
    send_mail( subject, message, email_from, recipient_list)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send, 'interval', days=3)
    scheduler.start()