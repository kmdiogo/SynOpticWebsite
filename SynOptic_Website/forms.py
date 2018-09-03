from django import forms
from .constants import SCALE_CHOICES,SONGLENGTH_CHOICES

class MIDIConfig(forms.Form):
    fileName = forms.CharField()
    image = forms.ImageField()
    scale = forms.ChoiceField(choices=SCALE_CHOICES)
    length = forms.ChoiceField(choices=SONGLENGTH_CHOICES)
