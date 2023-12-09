from django import forms
from django.contrib.auth.models import User


# class LoginForm(forms.Form):
#     username = forms.CharField(label='Логин')
#     password = forms.CharField(label='Пароль')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class":"pass_field"}))
    password2 = forms.CharField(label='Повторите пароль',widget=forms.PasswordInput(attrs={"class":"pass_field"}))
    
    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']    