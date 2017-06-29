from django import forms
import re
from django.contrib.auth.forms import ReadOnlyPasswordHashField            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from user_profile.models import AirpactUser    
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def debuggin():
    return True

def usernameValidator(value):
    if value is None:
        return False 
    pattern = re.compile("^[0-9a-zA-Z]*$")
    return pattern.match(value)
 
# Custom user creation form for an Airpact User
class UserCreationForm(forms.ModelForm):
    confirm_email = forms.EmailField(label='Confirm Email', required = True, widget=forms.EmailInput)
    password = forms.CharField(label='Password', required = True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', required = True, widget=forms.PasswordInput)
    
    class Meta:
        model = AirpactUser

        # Note - include all *required* MyUser fields here,
        # but don't need to include password and confirm_password as they are
        # already included since they are defined above.
        fields = ('username','email')       
    

    def clean(self):
        
        if not usernameValidator(self.cleaned_data.get('username')):
            self.add_error('username', 'Username contains invalid characters')
        

        if 'confirm_email' in self.cleaned_data and self.cleaned_data['email'] != self.cleaned_data['confirm_email']:
            self.add_error('confirm_email', 'Email and Confirm Email fields must match')

        if 'confirm_email' in self.cleaned_data:
            if AirpactUser.objects.filter(email= self.cleaned_data['email']):
                self.add_error('email', "This email already used")

        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Password & Confirm Password fields must match.')

        return super(UserCreationForm, self).clean()

    def cleanUsername(self):
        if not usernameValidator(self.cleaned_data.get('username')):
            self.add_error('username', 'Username contains invalid characters. Usernames may only consist of letters')

    def save(self,commit = True):   
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        
        # Fields to be added later: 
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
    
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = AirpactUser
        fields = ['first_name', 'last_name', 'email','bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'})
        }
