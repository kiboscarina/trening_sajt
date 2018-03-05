from django.contrib import admin
from data.models import News
from data.models import Trainer, Training
from data.models import RegUser
from data.models import ScheduleTraining
from data.models import Rating



class TrainerDetails(admin.ModelAdmin):
    list_display = ('first_name' , 'last_name')
    search_fields = ('about', )    
admin.site.register(Trainer)

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('__str__', '')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('hedline',)
    search_fields = ('hedline','text')

admin.site.register(News, NewsAdmin) 
admin.site.register(Training)
admin.site.register(RegUser)
admin.site.register(ScheduleTraining)
admin.site.register(Rating)




