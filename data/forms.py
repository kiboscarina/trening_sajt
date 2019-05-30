from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from data.models import News
from data.models import Rating
from django.http.request import QueryDict
from data.validators import filter_za_reci

class UserRatingForm(forms.ModelForm):
    rating = forms.CharField()
    user_rating = forms.IntegerField(
        validators=[MaxValueValidator(5),
                    MinValueValidator(1)])

    def __init__(self, *args, **kwargs):
        print("proba args", args, "proba args")
        print('proba kwargs', kwargs, "proba kwargs")
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
# 
    class Meta:
        model = Rating
        fields = ('user_rating', 'rating')
  
  
  
class NewsForm(forms.ModelForm):
    text = forms.CharField(validators=[filter_za_reci])
    hedline = forms.CharField()
    picture = forms.FileField(required=False)


    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        

    def clean(self):
        data = self.cleaned_data
        return data
    



    class Meta:
        model = News
        fields = ('hedline', 'text', 'picture',)




class NewsFormGet(forms.ModelForm):
    text = forms.CharField()
    hedline = forms.CharField()
    picture = forms.FileField(required=False)


    class Meta:
        model = News
        fields = ('hedline', 'text', 'picture',)







































        
