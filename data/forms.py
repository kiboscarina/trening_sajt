from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from pip._vendor.requests.api import post

from data.models import Rating, Trainer, RegUser


class UserRatingForm(forms.ModelForm):
    rating = forms.CharField()
    user_rating = forms.IntegerField( 
                                validators=[MaxValueValidator(5),
                                            MinValueValidator(1)])

    def __init__(self, *args, **kwargs):        
        self.user = kwargs['user']
        self.trainer = kwargs['trainer']
        del kwargs['user']
        del kwargs['trainer']
        super(UserRatingForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        data = self.cleaned_data
        data['user'] = self.user
        data['trainer'] = self.trainer
        return data
    
    class Meta:
        model = Rating
        fields = ('user_rating', 'rating')
        