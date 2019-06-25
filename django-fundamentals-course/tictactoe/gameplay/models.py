from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from pip.cmdoptions import editable
from django.core.validators import MinValueValidator, MaxValueValidator

# Liste des options possibles pour une game
GAME_STATUS_CHOICES = [
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
    ]

# Taille d'une board 
BOARD_SIZE = 3

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
    
    def board(self):
        """
        Methode permettant de retourner une matrice 3x3 contenant l'ensemble des moves
        faits par les utilisateurs 
        """
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        # Comme Move a une foreign key dans game je peux atteindre la liste des moves
        # depuis game
        for move in self.move_set.all():
            board[move.y][move.x] = move
        
        return board
    
    def is_users_move(self, user):
        return (user == self.first_player and self.status == 'F') or \
            (user == self.second_player and self.status == 'S' )
            
    
    # Permet de construire l'url qui représente cette game
    def get_absolute_url(self):
        return reverse('gameplay_detail', args=[self.id])
    
    def new_move(self):
        """
        Permet de créer un nouveau move associé à la game
        """
        # On vérifie si la game n'est pas finie
        if self.status not in 'FS':
            raise ValueError("Cannot make move on a finished game")
        
        # On retourne le Move prérempli
        return Move(
            game=self,
            by_first_player=self.status == 'F')
    
    def update_after_move(self, move):
        self.status = self._get_game_status_after_move(move)
    
    def _get_game_status_after_move(self, move):
        """
        Methode permettant de mettre a jour l'etat de la game
        Gagne perdu ou Draw
        """
        x, y = move.x, move.y
        board = self.board()
        if (board[y][0] == board[y][1] == board[y][2]) or \
            (board[0][x] == board[1][x] == board[2][x]) or \
            (board[0][0] == board[1][1] == board[2][2]) or \
            (board[0][2] == board[1][1] == board[2][0]):
            return 'W' if move.by_first_player else 'L'
        if self.move_set.count() >= BOARD_SIZE**2:
            return 'D'
        # Cas ou la game doit continuer
        return 'S' if self.status == 'F' else 'F'
            
    
    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)

class Move(models.Model):
    x = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE-1)]
        )
    y = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE-1)]
        )
    # Déclare dans la DB SQL Lite un char d'une taille max de 300 non obligatoire
    comment = models.CharField(max_length = 300, blank = True)
    # Champs permettant de déterminer si le move a été fait par le joueur 1
    by_first_player = models.BooleanField(editable = False)
    # Un move sera associé à une game, de manière automatique une game aura un set de move
    # Si la game est supprimée, les moves associes aussi
    game = models.ForeignKey(Game, on_delete = models.CASCADE, editable=False)
    
    def __eq__(self, other):
        """
        Methode permettant dutiliser le == sur move
        Prend en parametre le other qui est le deuxime move de l'egalite
        """
        if other is None:
            return False
        # Retourne vrai si les 2 moves sont faits par le meme joueur
        return other.by_first_player == self.by_first_player
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la methode save qui sera appelee a chaque fois qu'un move
        est save
        """
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()
        
    
    