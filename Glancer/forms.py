from django import forms
from .models import Glance, Profile



class SendGlance(forms.Form):
    recipient = forms.ModelChoiceField( label='', queryset=Profile.objects.all().order_by('user__first_name'))
    description = forms.CharField(label='', widget=forms.Textarea)