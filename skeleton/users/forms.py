from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Form class required for User Django Admin.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name',
                  'is_active', 'is_admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form class required for User Django Admin.
    """
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"password/\">this form</a>.")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class SignupForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=60,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'autofocus': 'autofocus'}))

    def signup(self, request, user):
        email = self.cleaned_data['email']
        user.email = email
        user.save()
