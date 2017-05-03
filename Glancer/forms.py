from django import forms
from .models import Glance, Profile



class SendGlance(forms.Form):

    recipient = forms.ModelChoiceField(label='Select the Lucky Person', queryset=Profile.objects.order_by('user__first_name'))
    description = forms.CharField(label='Describe something special this person did', widget=forms.Textarea)

class AnonymousReview(forms.Form):

    review = forms.CharField(label='Please give an honest and truthful review towards your Employer', widget=forms.Textarea)
