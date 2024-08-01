from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import LoginForms, RegisterForms
from .models import Profile

#Authentication
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Create your views here.

#Login
def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            login_username = form['login_username'].value()
            password = form['password'].value()

        user = auth.authenticate(
            request,
            username=login_username,
            password=password
        )
        if user is not None:
            auth.login(request, user)
            return redirect('userOrders--page')
        else:
            return redirect('login')

    return render(request, 'login_page.html', {'form': form})

#logout 
def logout(request):
    auth.logout(request)
    return redirect('login')

    
#Register

def register(request):
    form = RegisterForms()

    if request.method == 'POST':
        form = RegisterForms(request.POST)

        if form.is_valid():
            username=form['username'].value()
            email=form['email'].value()
            password_1=form['password_1'].value()

            if User.objects.filter(username=username).exists():
                return redirect('register')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password_1,
            )
            user.save()
            return redirect('create__artists')

    return render(request, 'register.html', {'form': form})

def registerEditor(request):
    form = RegisterForms()

    if request.method == 'POST':
        form = RegisterForms(request.POST)

        if form.is_valid():
            username=form['username'].value()
            email=form['email'].value()
            password_1=form['password_1'].value()

            if User.objects.filter(username=username).exists():
                return redirect('register')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password_1,
            )
            user.save()
            return redirect('createEditor')

    return render(request, 'register.html', {'form': form})

#Create Photographer
class ServicesCreateArtists(GroupRequiredMixin,LoginRequiredMixin,CreateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        fields = ["username", "firstName", "lastName", "phoneOne", "phoneTwo", "addressOne", "addressTwo", "zipCode", "city", "state"]
        template_name = "completeProfile.html"
        success_url = reverse_lazy('listArtists')

#Update Photographer 
class ProfileUpdate(GroupRequiredMixin,LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Admin" u"EquipMember"]
    template_name = "completeProfile.html"
    model = Profile
    fields = ["username", "firstName", "lastName", "phoneOne", "phoneTwo", "addressOne", "addressTwo", "zipCode", "city", "state"]
    success_url = reverse_lazy("listArtists")

#Create Editor
class CreateEditor(GroupRequiredMixin,LoginRequiredMixin,CreateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        fields = ["username", "firstName", "lastName", "phoneOne", "phoneTwo", "addressOne", "addressTwo", "zipCode", "city", "state"]
        template_name = "completeProfile.html"
        success_url = reverse_lazy('listEditor')
