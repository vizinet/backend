from django import forms
from django.db.models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)
