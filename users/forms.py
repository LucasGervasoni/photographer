# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError

# class UserForm(UserCreationForm):
#   email = forms.EmailField(max_length=100)
  
#   class Meta:
#     model = User
    
#   def clean_email(self):
#     e = self.cleaned_data['email']
#     if User.objects.filter(email=e).exists():
#       raise ValidationError("The E-mail {} is already in use".format(e))
    
#     return e