from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerField, Model
from django.db.models.signals import post_save
from allauth.utils import get_username_max_length


class Trainer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    picture = models.FileField(upload_to='users_pic', null=True, blank=True)
    email = models.CharField(max_length=1000)
    phone = models.CharField(max_length=50)
    about = models.CharField(max_length=2048) 
    creditcard = models.CharField(max_length=255)
    short_massage = models.CharField(max_length=128, null=True, blank=True)
    average_value = models.DecimalField( max_digits=3, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.first_name



class News(models.Model):
    class Meta:
        verbose_name_plural = 'news'
    hedline = models.CharField(max_length=255)
    text = models.TextField() 
    picture = models.FileField(upload_to='news_pic', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.hedline


class Training(models.Model):
    class Meta:
        verbose_name_plural = 'Training'
    trainer = models.ForeignKey(Trainer)
    name = models.CharField(max_length=128, null=True, blank=True)
    duration = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.CharField(max_length=512)
    location = models.CharField(max_length=255)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6) 
    training_image = models.FileField(upload_to='.', null=True, blank=True)
    
    def __str__(self):
        return '{}: {}'.format(self.name, self.trainer)   
    
class RegUser(models.Model):
    user = models.ForeignKey(User)
    trainer = models.ForeignKey(Trainer, null=True, blank=True)
    profilePicture = models.FileField(upload_to='users_pic', null=True, blank=True)
    def __str__(self):
        return self.user.first_name

def create_profile(sender, **kwargs):
    print(kwargs)
    if kwargs['created']:
        reguser = RegUser.objects.create(user=kwargs['instance'])
        
post_save.connect(create_profile, sender=User)
    
      
class ScheduleTraining(models.Model):  
    training = models.ForeignKey(Training, null=True, blank=True)
    reguser = models.ForeignKey(RegUser, null=True, blank=True)
#     user = models.ForeignKey(RegUser, null=True, blank=True)

    def __str__(self):
        return '{} - {}#{}'.format(
            self.reguser.user.first_name,
            self.training.type,
            self.training.pk
        )



class Rating(models.Model):
    userrating = (
        ('1','very bad'),
        ('2','bad'),
        ('3','medium'),
        ('4','good'),
        ('5','over 9000'),
    )
    user_rating = IntegerField( 
                                validators=[MaxValueValidator(5),
                                            MinValueValidator(1)])
    rating = models.CharField(max_length=512)
    user = models.ForeignKey(RegUser, null=True, blank=True)
    trainer = models.ForeignKey(Trainer) 

    def __str__(self):
#         return self.trainer.first_name
        return '{}: {}'.format(self.trainer.first_name , self.user_rating)            

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        print('STA SE DESILO', self.user)
        all_ratings = self.trainer.rating_set.all()
        values = all_ratings.values_list('user_rating', flat=True)
        suma = sum(list(values))
        self.trainer.average_value = suma / len(all_ratings)
        self.trainer.save()
    
    def get_full_name(self):
        return 'NAME'
















