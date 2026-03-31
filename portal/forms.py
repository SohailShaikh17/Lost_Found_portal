from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Item, ClaimRequest

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    department = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','department','phone_number']
    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.department = self.cleaned_data.get('department','')
            profile.phone_number = self.cleaned_data.get('phone_number','')
            profile.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','department','phone_number']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user','created_at','updated_at']
        widgets = {'date_of_event': forms.DateInput(attrs={'type':'date'})}

class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['message','proof_note']
