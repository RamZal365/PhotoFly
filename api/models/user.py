from django.contrib.auth.models import User
from django.db import models
from api.models.game import Game


class CustomUser(User):
    game = models.ForeignKey(Game, related_name='users', null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    has_played = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

