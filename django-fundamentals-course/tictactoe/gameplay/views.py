from django.shortcuts import render, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required
# Create your views here.

# Vue en charge d'afficher une partie
@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    return render(request,
                  "gameplay/game_details.html",
                  {'game' : game})
