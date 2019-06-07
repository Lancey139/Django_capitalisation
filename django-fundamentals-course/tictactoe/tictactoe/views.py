"""
Exemple de creation de vue par fonction
"""

from django.shortcuts import render

def welcome(request):
    return render(request, 'tictactoe/welcome.html')