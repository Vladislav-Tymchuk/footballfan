from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from django.db import models

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=250, help_text='например, aaaaa@gmail.com')
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2')


	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('Пароли не совпадают')
		return cd['password2']

	def clean_email(self):
	    email = self.cleaned_data.get('email')
	    if User.objects.filter(email=email).exists():
	        raise forms.ValidationError('Почта уже существует')
	    return email

	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError('Данный пользователь уже существует')
		return self.cleaned_data['username']

 
class CommentForm(forms.ModelForm):
    content = forms.CharField()
    
    class Meta:
        model = Comment
        fields =['content']
