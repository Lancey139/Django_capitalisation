from django.forms import ModelForm
from .models import Move

class MoveForm(ModelForm):
    class Meta:
        model = Move
        # Les classes héritant de ModelForm doivent toujours avoir soit
        # un include soit un exclude meme s'il est vide
        exclude = [] 