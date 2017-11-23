from django import forms 
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout, 
)   

User = get_user_model()
class UserLoginView(forms.Form):
    username = forms.CharField() 
    password = forms.CharField(widget= forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password :
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('Input Error')
            if not user.check_password(password):
                raise forms.ValidationError('Input Error')
            if not user.is_active:
                raise forms.ValidationError('this user in not longer active')
        return super(UserLoginView,self).clean(*args,**kwargs)

class UserRegisterView(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',

        ]


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2 :
            raise forms.ValidationError('password must match')
        return password
