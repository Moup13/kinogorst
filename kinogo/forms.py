from django.forms.models import ModelForm

from kinogo.models import (
    Movie
)


class ProductForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('__all__')
        exclude = ['slug']


# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(help_text='A valid email address, please.', required=True)
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#
#         user = super(UserRegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#
#         return user
#
#     def __init__(self, *args, **kwargs):
#
#         super(UserRegistrationForm, self).__init__(*args, **kwargs)
#
#
# class UserLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', False)
#         super(UserLoginForm, self).__init__(*args, **kwargs)
#
#     username = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
#         label="Username or Email*")
#
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': 'Password'}))
#
#     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
#
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#     image = forms.ImageField(required=False, widget=forms.FileInput)
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username','email', 'image']


from django import forms


# from .models import SignUp

class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()
