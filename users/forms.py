from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from dataclasses import fields

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'teste@gmail.com'})) #compulsory
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter your username'})) #compulsory
    password1 = forms.CharField(required=True,widget=forms.PasswordInput()) #compulsory
    password2 = forms.CharField(required=True,widget=forms.PasswordInput()) #compulsory
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and User.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError('This username is alread in use')
        return username

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is alread in use')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError('Password is too short')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2   


    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)

        #user.username = self.clean_username
        
        print(user.username)
        #print(user['email'])
        #print(user.password1)
        #print(user.password2)
        
    
        user.email = self.cleaned_data['email'] #clean the email
        if commit:
            user.save()
        return user