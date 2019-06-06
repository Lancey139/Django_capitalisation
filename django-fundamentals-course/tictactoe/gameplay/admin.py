# Register your models here.
# Ce fichier est utile pour personaliser l'interface administrateur

from django.contrib import admin
from .models import Game, Move

# On créé une classe qui va permettre de personaliser l'interface admin pour les games
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_player', 'second_player', 'status')
    list_editable = ('status', )

admin.site.register(Move)

