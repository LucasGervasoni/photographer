from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

#Login Form
class LoginForms(forms.Form):
    login_username=forms.CharField(
        label='Username', 
        required=True, 
        max_length=100,
    )
    password=forms.CharField(
        label='Password', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput()
    )

#Register Form
class RegisterForms(forms.ModelForm):
    password_1 = forms.CharField(
        label='Password',
        required=False,  # Initially set to False; we'll adjust this in __init__
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_2 = forms.CharField(
        label='Confirm your Password',
        required=False,  # Initially set to False; we'll adjust this in __init__
        max_length=70,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_1', 'phone_2', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If we're updating an existing user, passwords are optional
            self.fields['password_1'].required = False
            self.fields['password_2'].required = False
        else:
            # If we're creating a new user, passwords are required
            self.fields['password_1'].required = True
            self.fields['password_2'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        if password_1 or password_2:
            if password_1 != password_2:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data