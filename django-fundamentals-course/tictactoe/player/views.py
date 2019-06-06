from django.shortcuts import render
from gameplay.models import Game
# Create your views here.

def home(request):
    # On récupère toutes les parties pour lesquelles l'utilisateur doit jouer
    
    # Ce code n'est pas terrible car il brise plusieurs concept:
    # -> Le concept du lazy Query Set qui permet d'executer au minimum le code SQL
    # Ici le code est exécuter avec le cast en list
    # -> Le concept MTV : Model Templates View est brisé ici car on créer un 
    # model dans la partie view
    games_first_player = Game.objects.filter(
        first_player=request.user,
        status='F')
    games_second_player = Game.objects.filter(
        second_player=request.user,
        status='S')
    all_my_games = list(games_first_player) + list(games_second_player)
    
    # Pour palier à ca, la responsabilité de tratier les datas est déplacées dans
    # le manager de game dans le models.py
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    
    # Le chemin est relatif au dossier template de l'app
    return render(request, "player/home.html",
                  {'games' : active_games})