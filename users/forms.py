from django import forms

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
class RegisterForms(forms.Form):
    username=forms.CharField(
        label='Username',
        required=True,
        max_length=100,
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
    )
    password_1=forms.CharField(
        label='Password', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_2=forms.CharField(
        label='Confirm your Password', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput()
    )
    
    
    def clean_username_login(self):
        nome = self.cleaned_data.get('login_username')

        if nome:
            nome = nome.strip()
            if ' ' in nome:
                raise forms.ValidationError('Spaces are not allowed in this field')
            else:
                return nome

    def clean_password(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')

        if password_1 and password_2:
            if password_1!= password_2:
                raise forms.ValidationError('Passwords are not the same')
            else:
                return password_2