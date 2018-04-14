from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(forms.ModelForm):
    description = forms.CharField(help_text='Required')
    degree = forms.CharField(help_text='Degree Required')

    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'role', 'description', 'degree')