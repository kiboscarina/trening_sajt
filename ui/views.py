from datetime import datetime, date, timedelta
import decimal
import json
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Sum
from django.http.response import Http404, HttpResponse
from django.shortcuts import render , redirect
from django.template.context_processors import request
from django.views.generic.base import TemplateView
from requests.api import post
from data.forms import UserRatingForm
from data.models import News, Training, RegUser, Rating, Trainer
from data.models import ScheduleTraining
from data.tasks import moj_task, notify_participants_about_training_cancelation
from data.utils import get_trainer_ratings
from ui.forms import TrainingForm
from vezbacki.celery_wrapper import CELERY_DELAY, CELERY_ASYNC

# Prikazivanje  svih aktivnih usera
# 
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone



def trener(request):
    if request.user.is_authenticated():
        return RegUser.objects.filter(user=request.user).first().trainer

def training(request):
    return render( request,template_name= 'index.html') 

def custom_signup(request):
    return render(request, template_name='dalibor/forma.html')

def get_traning_locations(request):
    print(request.POST)
    lat = float(request.POST['lat'])
    lng = float(request.POST['lng'])
    x = 0.1
    training_found = Training.objects.filter(
        lat__gt=lat - x,
        lat__lt=lat + x,
        lng__gt=lng - x,
        lng__lt=lng + x,
    )
    relevant_data = training_found.values('lng', 'lat', 'trainer', 'type')
    relevant_data = list(relevant_data)
    for item in relevant_data:
        item['lng'] = float(item['lng'])
        item['lat'] = float(item['lat'])
        
    
    return HttpResponse(json.JSONEncoder().encode(relevant_data))





def index(request):
    
    def currentUsers():
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
        return User.objects.filter(id__in=user_id_list)
    
    queryset = currentUsers()
#     print(queryset)
#     print(queryset.exists())
#     print(queryset.count())
    if request.user.is_authenticated():
        reg_user = RegUser.objects.get(user = request.user)
#         print(reg_user)

    else:
        reg_user = None
    news = News.objects.all().order_by('-id')[:4]
#     ratings = get_trainer_ratings()
    trainersWithGrade = Trainer.objects.filter(~Q(average_value=None))
    top_trainers = trainersWithGrade.order_by('-average_value')[:3]
    
    
    built_context = {
        'queryset':queryset,
        'news':news,
        'top_trainers' : top_trainers,
        'reg_user' : reg_user,
    }
    

    return render(request , template_name='index.html', context=built_context)
    
  
  

    
def log(request):
    if request.user.is_authenticated():
        return render(request , template_name= 'ui/index.html')
       
    
def treneri(request):
    trainer = Trainer.objects.all() 
    built_context = {
        'svi':trainer
    }
    if request.user.is_authenticated():
        return render(request , template_name= 'page.html' , context=built_context)    
    else:
        raise Http404('log in ')
     
def default(o):
    if type(o) is date or type(o) is datetime:
        return o.isoformat()
    

def trainerZaAjaks(request, trainer_id):
    print(request.POST)
    trainer = Trainer.objects.filter(pk=trainer_id).first()
    training_found = trainer.training_set.all().order_by('-start')[:10]
    relevant_data = training_found.values('lng', 'lat', 'type', 'duration', 'start', 'end')
#     relevant_data[4] = relevant_data[4].time()
    
    relevant_data = list(relevant_data)
    for item in relevant_data:
        item['lng'] = float(item['lng'])
        item['lat'] = float(item['lat'])
        item['start'] = default(item['start'])
        item['end'] = default(item['end'])
    
    return HttpResponse(json.JSONEncoder().encode(relevant_data))

def trainer(request, trainer_id):
    trainer = Trainer.objects.filter(pk=trainer_id).first()
    trainings = trainer.training_set.all().order_by('-start')[:4]
    reg_user = RegUser.objects.filter(user=request.user).first()
    if not reg_user:
        return Http404('ne postoji Reg user za ulogovanog korisnika')
    print(trainings)
    if trainer:
        built_context = {
            'trainer': trainer,
            'trainings': trainings,
            'reg_user': reg_user,
        }
        
        return render(request , template_name='trainer.html' , context=built_context)    
    else:
        raise Http404('nema trenera ')
    
# samo mi daje news iz baze    
def wholenews(request , news_id):   
    news = News.objects.filter(pk=news_id).first()
    if news:
        built_context = { 'news': news }
        return render(request , template_name= 'wholenews.html' , context=built_context)    
    else:
        raise Http404("OOPS")
    
#  ova funkcija sluzi tome da kad  klijent klikne na ime nekog treninga
#  moze da vidi koliko je ljudi prijavljeno za isti.
def selectedTraining(request, training_id, RegUser_id):
    r_user = RegUser.objects.filter(pk=RegUser_id).first()
    training = Training.objects.filter(pk=training_id).first()
    scheduletraining = ScheduleTraining.objects.filter(training=training)
#     print('AAAAAAAAAAAA', training)
    built_context = {
            'training': training,
            'r_user': r_user,
            'scheduletraining': scheduletraining,
        }
    return render( request, template_name= 'trainingStats.html',context=built_context) 



def userProfile(request):
    if request.user.is_authenticated():
#         print('unutar IF')
        reg_user = RegUser.objects.filter(user=request.user).first()
        all_scheduled = list(reg_user.scheduletraining_set.all())
#         print(all_scheduled)
        trainers = []
        for t in all_scheduled:
#             print(t)
            svi_prijavljeni = t.training.scheduletraining_set.all()
            for prijava in svi_prijavljeni:
#                 print('\t', prijava.reguser)
#  all_scheduled--mi dobavlja sve treninge na koji je ulogovani user registrovan
#  svi prijavljeni --mi dobavjla sve prijavljene usere na treninge na kojima je ulogovanii user
# prijavljlen
#         if (len(all_scheduled)) >= 3: 
                for x in all_scheduled:
#             print('ZA X = ', x, end=' ---> ')
                    if x.training.trainer not in trainers:
                        trainers.append(x.training.trainer)
    else:
        print('unutar ELSE')
        reg_user = None
        all_scheduled = []
        trainers = []
    
    # ovde zavrsava if statement
    built_context = {
        'reg_user': reg_user,
        'all_scheduled': all_scheduled,
        'trainers':trainers,
    }
    return render(request , template_name= 'userprofile.html', context=built_context)














 
# class userRevievForm(TemplateView):
#     template_name = 'userrating.html'
#     
#     def get(self,request, trainer_id):
#                 form = userRevievForm()
#                 return render(request, self.template_name, {'form' :form}) 
#      
#     def post(self, requst):
#         form = userRevievForm(requst.POST)
#         if form.is_valid():
#             text = form.cleaned_data['user_rating','rating'] 
#         args = {'form' :form, 'text' : text}      
#         return render(request, self.template_name, args) 
    
    
    


   
   
   
#    
class userrating(TemplateView):
    template_name = 'userrating.html'
     
    def get(self, request, trainer_id):
        form = UserRatingForm()
        return render(request, self.template_name, {'form' :form}) 

    def post(self, request, trainer_id):
        form = UserRatingForm(
            request.POST,
            user=RegUser.objects.get(user=request.user), 
            trainer=Trainer.objects.get(pk=trainer_id)
        )

        if form.is_valid():
            Rating.objects.create(**form.cleaned_data)
            
            text = form.cleaned_data['rating']
            args = {'form' :form, 'text' : text}
            return render(request, self.template_name, args) 
        else:
#             print(form.errors)
            return HttpResponse('NE VALJA {}'.format(form.errors))
   
   
   
   
    
    
def userProfilechannges(request):
    if request.method == 'POST':    
        m = RegUser.objects.filter(user=request.user).first()
        m.profilePicture.save(
            request.FILES['pic'].name,
            ContentFile(request.FILES['pic'].read())
        )
        return redirect('userProfile')
    else:
        return HttpResponse('ONLY POST ALLOWED')
    
#   prikazuje profil trenera 
def trainerProfilechannges(request):
    if request.user.is_authenticated():
        reg_user = RegUser.objects.filter(user=request.user).first()
#         print(trainer)
    built_context = {
        'reg_user': reg_user,
    }
    return render( request, template_name= 'trainerprofile.html', context=built_context) 
        
#    prikazuje ko se od usera prijavio na trening moze da bude ista ko i selectedTraining!!
#  a zapravo i salju na istu stranu!!!!


def trainingStats(request, training_id):
#     r_user = RegUser.objects.filter(pk=training_id).first()
    training = Training.objects.filter(pk=training_id).first()
    scheduletraining = ScheduleTraining.objects.filter(training=training)
#     print('AAAAAAAAAAAA', training)
    built_context = {
            'training': training,
#             'r_user': r_user,
            'scheduletraining': scheduletraining,
        }
    return render( request, template_name= 'trainingStats.html', context = built_context) 
 
 
     
def zakazaniTrening(request, training_id):
# urce    requser=request.POST.get('date','')
    r_user = RegUser.objects.filter(user=request.user).first()
    training = Training.objects.filter(pk=training_id).first()
    if ScheduleTraining.objects.filter(reguser=r_user, training=training):
        messages.success(request,'you are already registered');
# ovde treba da se sredi error massage
    else:
        ScheduleTraining.objects.create(
            training=training,
            reguser=r_user,
        )
    return render( request, template_name= 'index.html') 



def newTrainingForm(request):
    Template_name = 'newTrainingForm.html'
    if request.method == 'GET':
        form = TrainingForm()
        return render(request, Template_name, {'f': form})
    

    elif request.method == 'POST':
        trainer = RegUser.objects.filter(user=request.user).first()
        form = TrainingForm(request.POST, request.FILES, user=request.user)
        regUser = RegUser.objects.filter(user=request.user).first()  
        if form.is_valid():
            training_obj = form.save(commit=False)
            training_obj.start = form.cleaned_data['start']
            training_obj.end = form.cleaned_data['end']
            training_obj.trainer = regUser.trainer
            training_obj.save()
            training_obj.training_image.save(
                 request.FILES['training_image'].name,
                 request.FILES['training_image'].file,
                 save=True,
            )
# ovde trebam da stavim kad ce mail da se salje
            CELERY_ASYNC(
                notify_participants_about_training_cancelation,
#                 staviti u varijablu vreme- vreme iz tabele kad se 
#                 trening odrzava i dodati sat vremena vise!! i tad da se
#                 startuje func!!! ili ti samo da dodam valjda time delta -1
                eta=datetime.now() + timedelta(seconds=120),
                args=[training_obj.id],
            )


            messages.info(request, 'USPESNO STE NAPRAVILI TRENING')
            return redirect('/')
        else:
            a = []
            print('ERRORS', form.errors.items())
            for key, value in form.errors.items():
                print(key, value)
                a.append('{}: {}'.format(key, value))
             
#             return HttpResponse('<br>'.join(a))
         
            return render(request, Template_name, {'f': form})
      
               
        
def proba(request):       
    return render(request, template_name= 'proba.html')     
     
     
         
        
def proveraKoJeBioNaTreningu(request):
    regu = request.user.reguser_set.first()
    trening = regu.trainer.training_set.filter(name='6-7').first()
#     niz = trening.scheduletraining_set.all()
    niz= list(trening.scheduletraining_set.all())
#     return HttpResponse('ok')
    built_context = {
        'niz': niz,
        'regu': regu,
        'trening': trening,
         }
    return render(request, template_name= 'emailVeryfier.html', context =  built_context )


def sejvzaprisutnekorisnike():
    return HttpResponse('aka')



def uplate():
        return HttpResponse('uplata')

     
    
    
    
    
    