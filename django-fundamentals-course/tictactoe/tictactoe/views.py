"""
Exemple de creation de vue par fonction
"""

from django.shortcuts import render, redirect

def welcome(request):
    """
    Page d'acceuil
    """
    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, 'tictactoe/welcome.html')