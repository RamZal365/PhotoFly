from django.contrib import admin

from api.models.game import Game
from api.models.user import CustomUser

admin.site.register(Game)
admin.site.register(CustomUser)
