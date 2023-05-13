from django.db import models
from api.choices import STATE


class Game(models.Model):
    code = models.CharField(max_length=6)
    round = models.PositiveIntegerField()
    state = models.PositiveIntegerField(choices=STATE)

    def start_game(self):
        self.state = STATE.UPLOADING_IMAGES
        self.save()
        game_users = self.users.all()
        for game_user in game_users:
            game_user.score = 0
            game_user.save()

    def init_game(self):
        self.state = STATE.INITIATED
        self.round = 1
        self.save()

    def next_round(self):
        self.round += 1


class GameImage(models.Model):
    from api.models.user import CustomUser
    game = models.ForeignKey(Game, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_images/')
    played = models.BooleanField(default=False)

    def __str__(self):
        return self.image.name

