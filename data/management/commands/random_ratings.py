import random

from django.core.management.base import BaseCommand

from data.models import Rating, RegUser, Trainer


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for i in range(30):
            ocena = random.randint(1, 5)
            komentar = 'Dajem ocenu {}!'.format(ocena)
            
            users = RegUser.objects.all()
            user_index = random.randint(0, len(users) - 1)
            user = users[user_index]
            
            treneri = Trainer.objects.all()
            trener_index = random.randint(0, len(treneri) - 1)
            trener = treneri[trener_index]
            
            data = {
                "user_rating": ocena,
                "rating": komentar,
                "user": user,
                "trainer": trener,
            }
            Rating.objects.create(**data)