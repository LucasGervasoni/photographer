from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
# from django.contrib.auth.models import User, Group
# from .forms import UserForm
from django.urls import reverse_lazy

# from .models import Profile

# Create your views here.
class UserCreate(CreateView):
    template_name = "/main_crud/admin/services__create--artists.html"
    # form_class = UserForm
    success_url = reverse_lazy('login_page')
    
# class ProfileUpdate(UpdateView):
#     template_name = "/main_crud/admin/services__create--artists.html"
#     # model = Profile
#     fields = ["nome_completo", "cpf", "telefone"]
#     success_url = reverse_lazy("index")
