from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ad, ExchangeProposal
from .models import User  


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  
        fields = ["username", "email"]  

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    title = forms.CharField(max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea)
    image_url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=Ad.AD_CATEGORIES)
    condition = forms.ChoiceField(choices=Ad.AD_CONDITIONS)

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal  
        fields = ['sender_ad', 'receiver_ad', 'comment']  
        widgets = { 
            'comment': forms.Textarea(attrs={'rows': 3})  
        }  

