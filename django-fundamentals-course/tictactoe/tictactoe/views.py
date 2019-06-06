"""
PExemple de creation de vue par fonction
"""

from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Hello, world ! ")