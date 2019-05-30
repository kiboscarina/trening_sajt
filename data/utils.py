from django.db.models.query_utils import Q
from data import models
from datetime import datetime, date, timedelta
import re
from django.utils.html import strip_tags
import math


def get_trainer_ratings():
    '''
        this function collects all trainer ratings and returns a dictionary
        return: 
        [
            {
                "trainer_id": trainer.id,
                "name": trainer.name,
                "average_rating": avg_rating,
            },
            ...
        ]
    '''
    def calc_average_rating(reg_user):
        all_ratings = reg_user.trainer.rating_set.all()
        print("boki je jebena legenda!!!!", all_ratings)
        values = all_ratings.values_list('user_rating', flat=True)
#         max_ratings = reg_user.trainer.rating_set.all().aggregate(Max('user_rating'))
#         print(max_ratings)
        suma = sum(list(values))
#         print(suma)
#         print(all_ratings)
        return suma / len(all_ratings)
    return_list = []
    all_trainers = models.RegUser.objects.filter(~Q(trainer=None))
    for reg_user in all_trainers:
        trainer_obj = {}
        trainer_obj['trainer_id'] = reg_user.trainer.id
        trainer_obj['name'] = reg_user.user.first_name
        trainer_obj['average_rating'] = calc_average_rating(reg_user)
        return_list.append(trainer_obj)
    return return_list

    
# return_list pravimo praznu LISTU
# all_trainers dobavlja sve registrovane usere koji nemaju trainer=None
# prolazimo petljom kroz sve dobavljene trenere i apendujemo ova 3 polja---pod imenom reg_user!!!!
# linija 33 poziva func iznad calc_average_rating i prosledjuje joj objekat trenera!!!
# u return_list listu pod imenom trainer_obj i vracamo je u Func



# all_ratings - dobija reg_usera kog smo provukli kroz petlju....
# values dobija all ratings koji uzima sve rejtinge datog trenera i pravi listu....
# (values je sad lista svih rejtinga za datog trenera)
  
  
#    a =  suma / len(all_ratings)
#         TOP_TRAINER = (Max(a))
#         return TOP_TRAINER

import datetime
import re
from django.utils.html import strip_tags

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+',word_string)
    count = len(matching_words)
    return count
    
def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)  # prosecno vreme citanja 
#     read_time_sec = read_time_min * 60 
#     read_time = datetime.timedelta(minutes=read_time_min)
#     vreme_string = read_time.strftime("%d/%m/%Y %H:%M:%S")
#     return vreme_string
    return read_time_min
    




