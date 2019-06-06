from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Liste des options possibles pour une game
GAME_STATUS_CHOICES = [
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
    ]

class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):
        # Méthode en charge de renvoyer un qury set contenant toutes les games
        # d'un utilisateur
        return self.filter(
            Q(first_player=user) | Q(second_player=user)
            )
    def active(self):
        #Methode qui retourne la liste des games actives
        return self.filter(
            Q(status='F') | Q(status='S')
            )

class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player" ,
                                      on_delete = models.CASCADE)
    second_player = models.ForeignKey(User, related_name="games_second_player",
                                       on_delete = models.CASCADE)
    
    start_time = models.DateTimeField(auto_now_add = True)
    last_active = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 1, default = 'F',
                              choices=GAME_STATUS_CHOICES)
    
    # On déclare le manager associé
    objects = GamesQuerySet.as_manager()
    
    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)
    
# Create your models here.
class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    # Déclare dans la DB SQL Lite un char d'une taille max de 300 non obligatoire
    comment = models.CharField(max_length = 300, blank = True)
    # Champs permettant de déterminer si le move a été fait par le joueur 1
    by_first_player = models.BooleanField()
    # Un move sera associé à une game, de manière automatique une game aura un set de move
    # Si la game est supprimée, les moves associes aussi
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    
    