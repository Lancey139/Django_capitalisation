from django.shortcuts import render, redirect, get_object_or_404
from gameplay.models import Game
from django.contrib.auth.decorators import login_required
from .forms import InvitationForm
from .models import Invitation
from django.core.exceptions import PermissionDenied

# Create your views here.

@login_required
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
    finished_games = my_games.difference(active_games)
    # On recupere les invitations qui sont recues par l'utilisateur
    # Les invitations sont directement liées à l'utilisateur donc on 
    # peut les récuperer grace a la foreignKey
    invitations = request.user.invitations_received.all()
    
    # Le chemin est relatif au dossier template de l'app
    return render(request, "player/home.html",
                  {'active_games' : active_games,
                   'finished_games': finished_games,
                   'invitations' : invitations})
    
@login_required
def new_invitation(request):
    if request.method == "POST":
        # L'utilisateur a rempli le form, il faut traiter les données
        # Avant tout on remplie les valeurs de l'invitation qui ne sont pas présentes dans
        # le form
        invitation = Invitation(from_user=request.user)
        
        # On vérifie si la data est valide en lui donnant un model prérempli avec l'utilisa
        # teur courant
        form = InvitationForm(instance=invitation, data=request.POST)
        # Cette méthode est tres importante et doit etre applée systématiquement
        # Si c'est valide on repart sur le home, sinon le form non validé est renvoyé
        # a l'utilisateur
        if form.is_valid():
            # On enregistre en data base
            form.save()
            return redirect("player_home")
    else:
        # L'utilisateur demande un nouveau FORM vierge, on lui affiche
        form = InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form':form})

@login_required
def accept_invitation(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user,
                )
        
        invitation.delete()
        # Redirection vers une mage ( url nommée player_home )
        #return redirect('player_home')
        # Appel de la méthode get_absolute_url du model game
        return redirect(game)
    else:
        return render(request,
                      "player/accept_invitation_form.html",
                      {'invitation' : invitation})
    
        


