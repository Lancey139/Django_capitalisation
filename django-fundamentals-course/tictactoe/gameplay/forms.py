from django.forms import ModelForm
from .models import Move
from django.core.exceptions import ValidationError

class MoveForm(ModelForm):
    class Meta:
        model = Move
        # Les classes héritant de ModelForm doivent toujours avoir soit
        # un include soit un exclude meme s'il est vide
        exclude = [] 
        
    def clean(self):
        """
        Methode permettant de rajouter des validations dans le form
        Attention toutefois car ces validations sont exéctuées avant les validations
        des modèles.
        """
        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        game = self.instance.game
        try:
            if game.board()[y][x] is not None:
                raise ValidationError("Square is not empty")
        except IndexError:
            raise ValidationError("Invalid coordinates")
        return self.cleaned_data