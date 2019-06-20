from django.shortcuts import render, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required
from .forms import MoveForm
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
