# from celery import task
# from celery.schedules import crontab
# from celery.task.base import periodic_task
# from django.core.mail import EmailMultiAlternatives
# 
# from data.models import Trainer
# 
# 
# @task
# def moj_task(*args):
#     print('----------- OVAJ TASK RADI', args)



from celery import task
from celery.schedules import crontab
from celery.task.base import periodic_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

from data.models import ScheduleTraining, RegUser
from data.models import Trainer
from data.models import Training


@task
def moj_task(*args):
    print('----------- OVAJ TASK RADI', args)
    
    
    
    
    
# @periodic_task(run_every=(crontab(minute='*', hour='*')))  # every 1 minute
# def spam():
#     print('SPAMUJEM SVAKI MINUT')




@task
def notify_participants_about_training_cancelation(training_id):
    training_obj = Training.objects.get(pk=training_id)
#     prijava = ScheduleTraining.objects.filter(training = training_obj).all()
    user = ScheduleTraining.objects.filter(training_id=training_id)
    dobijanje = user.reguser.all()
    for vezbac in dobijanje:
        print(vezbac.reguser)
    print('SHALJEM EMAIL', training_obj)
    

    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    