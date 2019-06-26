from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.contrib.auth.decorators import login_required
from .forms import MoveForm
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
# Create your views here.

# Vue en charge d'afficher une partie
@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    context = {'game' : game}
    if game.is_users_move(request.user):
        context ['form'] = MoveForm()
    return render(request,
                  "gameplay/game_details.html",
                  context)


# Vue en charge de faire le move
def make_move(request, id):
    game = get_object_or_404(Game, pk=id)
    if not game.is_users_move(request.user):
        raise PermissionDenied
    move = game.new_move()
    form = MoveForm(instance=move, data=request.POST)
    if form.is_valid():
        move.save()
        return redirect("gameplay_detail", id)
    else:
        return render(request,
                      "gameplay/game_details.html",
                      {'game' :game, 'form': form}
                      )
        
"""
La vue ci-dessous présente un exemple de view d'une classe
Ecrire des vues sous forme de classe permet d'heriter de template
deja fait  
"""
class AllGameList(ListView):
    model = Game