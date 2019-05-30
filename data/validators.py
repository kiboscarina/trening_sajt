from django.utils.translation import ugettext_lazy 
from django.core.exceptions import ValidationError
import requests
from django.shortcuts import render
from django.http.response import HttpResponse
from django.http.response import Http404, HttpResponse





# def validate_domainonly_email(value):
#     pass
# blacklist = ['jebanje', 'kurac']
#  
# def filter_za_reci(value):
#     if value in blacklist:
#         # raise VallidationError({'zabranjeno je koristiti ruzne reci'})
#         raise ValidationError({
#                 'zabranjeno je koristiti ruzne reci',
#             })
#  
#         return value






def filter_za_reci(value):
    payload = {'text' : value}
    r = requests.get('https://www.purgomalum.com/service/containsprofanity?',params=payload)
#     rez = r.text
    if r.text == 'true':
        print(r.text)
        print(r.content)
        raise ValidationError("zabranjeno je koristiti ruzne reci")
        
    else:
        print(r.text)
        print(r.headers)     
        return value
#         