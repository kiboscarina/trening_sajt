from datetime import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from datetimewidget.widgets import DateTimeWidget
from django import forms
from data.models import Training
from django.core.exceptions import ValidationError
from django.template.context_processors import request
from requests.api import post
from django.http.response import HttpResponse
from data.models import RegUser


class TrainingForm(forms.ModelForm):
    # DATE
    # 16 November, 2017
    # %d %B, %y
    DATE_INPUT_FORMATS = ('%d %B, %Y',)
    
    # TIME
    # 03:00PM
    #  
    TIME_INPUT_FORMATS = ('%I:%M%p',)
    
    name = forms.CharField(max_length=128)
    duration = forms.CharField(max_length=255)
    
    startD = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            attrs={'class': 'datepicker'}
        )
    )
    startT = forms.TimeField(
        input_formats=TIME_INPUT_FORMATS,
        widget=forms.TimeInput(
            attrs={'class': 'timepicker'}
        )
    )
    endD = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            attrs={'class': 'datepicker'}
        )
    )
    endT = forms.TimeField(
        input_formats=TIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            attrs={'class': 'timepicker'}
        )
    )
    type = forms.CharField(max_length=512)
    location = forms.CharField(max_length=255)
    lng = forms.DecimalField(max_digits=9, decimal_places=6)
    lat = forms.DecimalField(max_digits=9, decimal_places=6) 
    training_image = forms.FileField(required=False)
     
    class Meta:
        model = Training
        fields = [
            'name',
            'duration',
            'startD',
            'startT',
            'endD',
            'endT',
            'type',
            'location',
            'lng',
            'lat'
        ]




    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(self.user)
        super(TrainingForm, self).__init__(*args, **kwargs)
#         Super moze da se pise i bez argumenaTa!!!!!!!
#  pomocu __init sam odredio da ce ovo da mi bude prva metoda...Medjutim pomocu SUPER
# sa sam pozvao *args i**kwargs iz trening forme tako da sad u ovoj funkciji imam to na raspolaganju


    def clean(self):
        
        data = self.cleaned_data
        
        if 'startD' not in data:
            raise ValidationError('Invalid fields detected')
        elif 'startT' not in data:
            raise ValidationError('Invalid fields detected')
        elif 'endD' not in data:
            raise ValidationError('Invalid fields detected')
        elif 'endT' not in data:
            raise ValidationError('Invalid fields detected')
    
       
        start = datetime(
            year = data['startD'].year,
            month = data['startD'].month,
            day = data['startD'].day,
            hour = data['startT'].hour,
            minute = data['startT'].minute,
            second = data['startT'].second,
        )
        end = datetime(
            year = data['endD'].year,
            month = data['endD'].month,
            day = data['endD'].day,
            hour = data['endT'].hour,
            minute = data['endT'].minute,
            second = data['endT'].second,
        )
        data['start'] = start
        data['end'] = end
        
        del data['startD']
        del data['startT']
        del data['endD']
        del data['endT']
        print(data)
        
        regUser = RegUser.objects.filter(user=self.user).first()
        overlapping_trainings = training_overlap_check(**data, trainer=regUser.trainer)
        if overlapping_trainings:
            raise ValidationError({
                '__all__': 'Postoje treninzi koji se pokalapaju sa ovim vremenom',
            })
# dobijam reg usera preko__init__
# overlapping_trainings pozivam istoimenu funkciju i prosledjujem joj parametre
          
        return data
    
def training_overlap_check(start=None, end=None, trainer=None, **kwargs):
#     print('KWARGS koij sam dobio je!!!!!!', kwargs)
#     print('args koij sam dobio je!!!!!!',args)
#     print('TRAINER JE ', trainer)
    q1 = Training.objects.filter(trainer=trainer, start__gte=start, start__lt=end)
    q2 = Training.objects.filter(trainer=trainer, end__gt=start, end__lte=end)
    q3 = Training.objects.filter(trainer=trainer, start__lte=start, end__gte=end)
    return q1.union(q2).union(q3)
        
        
        
        

        
        
