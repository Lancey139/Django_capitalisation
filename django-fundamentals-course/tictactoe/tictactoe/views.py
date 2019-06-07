"""
Exemple de creation de vue par fonction
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def welcome(request):
    """
    Page d'acceuil
    La condition user.is_authenticated était utilisee avant le login_required
    Les 2 sont laissés à des fins pédagogiques mais cette condition n'est plus 
    utile avec ce code
    """
    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, 'tictactoe/welcome.html')