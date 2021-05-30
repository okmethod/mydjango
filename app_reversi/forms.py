from django import forms

from .models import GamePlayer

class GamePlayerForm(forms.ModelForm):

    class Meta:
        model = GamePlayer
        fields = ('name', 'image', 'color_r', 'color_g', 'color_b',)
