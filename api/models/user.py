from django.contrib.auth.models import User
from django.db import models

from api.models.game import Game


class CustomUser(User):
    game = models.ForeignKey(Game, related_name='users', on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

